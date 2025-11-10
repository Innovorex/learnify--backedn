"""
Materials Router
Handles upload, processing, and retrieval of teaching materials (PDF, DOCX, TXT)
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import os
from jose import JWTError, jwt

from database import get_db
from security import get_current_user, JWT_SECRET, JWT_ALGORITHM
from models import User
from models_materials import TeachingMaterial, MaterialChunk
from schemas_materials import (
    TeachingMaterialCreate,
    TeachingMaterialResponse,
    TeachingMaterialListResponse,
    MaterialUploadResponse,
    TeachingMaterialUpdate,
    FileProcessingStatus
)
from services.file_processor import FileProcessorService
from services.text_chunker import TextChunkerService
from services.vector_store_service import get_vector_store

router = APIRouter(prefix="/materials", tags=["Materials"])


# ============================================================
# CUSTOM AUTH FOR FILE PREVIEW (supports query parameter token)
# ============================================================
async def get_current_user_from_token_or_query(
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Authenticate user from query parameter token (for iframe requests)
    Falls back to standard header authentication
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from query parameter (for iframe)
    if not token:
        # If no query token, this will fail - iframe can't send Authorization headers
        raise credentials_exception

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# ============================================================
# BACKGROUND TASK: Process uploaded file
# ============================================================
async def process_uploaded_material(
    material_id: int,
    file_path: str,
    file_type: str
):
    """
    Background task to process uploaded material:
    1. Extract text from file
    2. Chunk text
    3. Create embeddings
    4. Store in Chroma DB
    """
    from database import SessionLocal
    db = SessionLocal()

    try:
        # Get material from database
        material = db.query(TeachingMaterial).filter(TeachingMaterial.id == material_id).first()
        if not material:
            print(f"❌ Material {material_id} not found")
            return

        # Update status to processing
        material.status = "processing"
        db.commit()

        print(f"🔄 Processing material {material_id}: {material.original_filename}")

        # Step 1: Extract text
        file_processor = FileProcessorService()
        extracted_text, metadata = await file_processor.process_file(file_path, file_type)

        if not extracted_text or len(extracted_text.strip()) < 50:
            raise Exception("No meaningful text could be extracted from the file")

        print(f"✅ Extracted {len(extracted_text)} characters")

        # Step 2: Chunk text
        text_chunker = TextChunkerService(chunk_size=1000, chunk_overlap=200)

        # Try to use page info if available from PDF
        if "page_texts" in metadata:
            chunks = text_chunker.chunk_with_page_info(extracted_text, metadata["page_texts"])
        else:
            chunks = text_chunker.chunk_text(extracted_text)

        print(f"✅ Created {len(chunks)} chunks")

        # Step 3: Create Chroma collection
        vector_store = get_vector_store()
        collection_name = vector_store.create_material_collection(material_id)

        # Step 4: Add chunks to Chroma
        chroma_ids = vector_store.add_chunks_to_collection(
            collection_name=collection_name,
            chunks=chunks,
            material_id=material_id
        )

        # Step 5: Save chunks to database
        for idx, chunk in enumerate(chunks):
            db_chunk = MaterialChunk(
                material_id=material_id,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.text,
                chunk_size=chunk.char_count,
                page_number=chunk.page_number,
                section_title=chunk.section_title,
                chroma_id=chroma_ids[idx]
            )
            db.add(db_chunk)

        # Step 6: Update material with results
        material.extracted_text = extracted_text[:10000]  # Store first 10k chars
        material.text_length = len(extracted_text)
        material.chunk_count = len(chunks)
        material.chroma_collection_name = collection_name
        material.extraction_metadata = metadata
        material.status = "completed"
        material.processed_at = datetime.utcnow()
        material.processing_error = None

        db.commit()

        print(f"✅ Successfully processed material {material_id}")

    except Exception as e:
        print(f"❌ Error processing material {material_id}: {str(e)}")

        # Update material with error
        material = db.query(TeachingMaterial).filter(TeachingMaterial.id == material_id).first()
        if material:
            material.status = "failed"
            material.processing_error = str(e)
            db.commit()

    finally:
        db.close()


# ============================================================
# UPLOAD MATERIAL
# ============================================================
@router.post("/upload", response_model=MaterialUploadResponse)
async def upload_material(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    grade_level: Optional[str] = Form(None),
    topics: Optional[str] = Form(None),  # Comma-separated
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a teaching material (PDF, DOCX, TXT)
    File will be processed in the background
    """
    # Verify user is a teacher
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can upload materials")

    # Process file
    file_processor = FileProcessorService()

    # Save file to disk
    file_path, filename, file_size = await file_processor.save_uploaded_file(file, current_user.id)

    # Get file type
    file_type = file_processor._get_file_extension(file.filename)

    # Parse topics
    topics_list = []
    if topics:
        topics_list = [t.strip() for t in topics.split(",") if t.strip()]

    # Create database record
    material = TeachingMaterial(
        teacher_id=current_user.id,
        filename=filename,
        original_filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        title=title,
        description=description,
        subject=subject,
        grade_level=grade_level,
        topics=topics_list,
        status="pending"
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    # Schedule background processing
    background_tasks.add_task(
        process_uploaded_material,
        material.id,
        file_path,
        file_type
    )

    return MaterialUploadResponse(
        material_id=material.id,
        filename=filename,
        original_filename=file.filename,
        file_size=file_size,
        status="pending",
        message="File uploaded successfully. Processing in background..."
    )


# ============================================================
# LIST MATERIALS
# ============================================================
@router.get("/", response_model=TeachingMaterialListResponse)
async def list_materials(
    page: int = 1,
    page_size: int = 20,
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all materials for the current teacher
    Supports filtering and pagination
    """
    # Build query
    query = db.query(TeachingMaterial).filter(TeachingMaterial.teacher_id == current_user.id)

    # Apply filters
    if subject:
        query = query.filter(TeachingMaterial.subject == subject)
    if grade_level:
        query = query.filter(TeachingMaterial.grade_level == grade_level)
    if status:
        query = query.filter(TeachingMaterial.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    materials = query.order_by(TeachingMaterial.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return TeachingMaterialListResponse(
        materials=materials,
        total=total,
        page=page,
        page_size=page_size
    )


# ============================================================
# GET MATERIAL BY ID
# ============================================================
@router.get("/{material_id}", response_model=TeachingMaterialResponse)
async def get_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific material by ID"""
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.id == material_id,
        TeachingMaterial.teacher_id == current_user.id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    return material


# ============================================================
# UPDATE MATERIAL METADATA
# ============================================================
@router.patch("/{material_id}", response_model=TeachingMaterialResponse)
async def update_material(
    material_id: int,
    update_data: TeachingMaterialUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update material metadata (title, description, etc.)"""
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.id == material_id,
        TeachingMaterial.teacher_id == current_user.id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Update fields
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(material, key, value)

    db.commit()
    db.refresh(material)

    return material


# ============================================================
# DELETE MATERIAL
# ============================================================
@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a material and its associated data"""
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.id == material_id,
        TeachingMaterial.teacher_id == current_user.id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Delete from Chroma DB
    if material.chroma_collection_name:
        vector_store = get_vector_store()
        vector_store.delete_material_collection(material.chroma_collection_name)

    # Delete file from disk
    file_processor = FileProcessorService()
    file_processor.delete_file(material.file_path)

    # Delete from database (cascades to chunks)
    db.delete(material)
    db.commit()

    return {"message": "Material deleted successfully"}


# ============================================================
# GET PROCESSING STATUS
# ============================================================
@router.get("/{material_id}/status", response_model=FileProcessingStatus)
async def get_processing_status(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check the processing status of an uploaded material"""
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.id == material_id,
        TeachingMaterial.teacher_id == current_user.id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Calculate progress
    progress = 0
    if material.status == "completed":
        progress = 100
    elif material.status == "processing":
        progress = 50
    elif material.status == "failed":
        progress = 0
    else:  # pending
        progress = 0

    message = {
        "pending": "Waiting to start processing...",
        "processing": "Extracting text and creating embeddings...",
        "completed": f"Successfully processed {material.chunk_count} chunks",
        "failed": "Processing failed"
    }.get(material.status, "Unknown status")

    return FileProcessingStatus(
        material_id=material.id,
        status=material.status,
        progress=progress,
        message=message,
        error=material.processing_error
    )


# ============================================================
# SERVE FILE FOR PREVIEW
# ============================================================
@router.get("/{material_id}/file")
async def get_material_file(
    material_id: int,
    current_user: User = Depends(get_current_user_from_token_or_query),
    db: Session = Depends(get_db)
):
    """
    Serve the original uploaded file for preview
    Returns the file with appropriate content-type for browser preview
    Accepts token as query parameter (?token=xxx) for iframe authentication
    """
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.id == material_id,
        TeachingMaterial.teacher_id == current_user.id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Check if file exists
    if not os.path.exists(material.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Determine media type
    media_type_map = {
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
    }

    file_ext = os.path.splitext(material.original_filename)[1].lower()
    media_type = media_type_map.get(file_ext, 'application/octet-stream')

    # Return file with inline disposition for preview
    return FileResponse(
        path=material.file_path,
        media_type=media_type,
        filename=material.original_filename,
        headers={
            "Content-Disposition": f'inline; filename="{material.original_filename}"'
        }
    )
