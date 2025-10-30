from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================
# ENUMS
# ============================================================

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


class MaterialStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================
# TEACHING MATERIALS SCHEMAS
# ============================================================

class TeachingMaterialBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Material title")
    description: Optional[str] = Field(None, description="Optional description")
    subject: Optional[str] = Field(None, max_length=200, description="Subject (e.g., Mathematics)")
    grade_level: Optional[str] = Field(None, max_length=100, description="Grade level (e.g., 10)")
    topics: Optional[List[str]] = Field(default_factory=list, description="List of topics covered")


class TeachingMaterialCreate(TeachingMaterialBase):
    """Schema for creating a new teaching material"""
    pass


class TeachingMaterialUpdate(BaseModel):
    """Schema for updating teaching material metadata"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    topics: Optional[List[str]] = None


class TeachingMaterialResponse(TeachingMaterialBase):
    """Schema for teaching material response"""
    id: int
    teacher_id: int
    filename: str
    original_filename: str
    file_type: FileType
    file_size: int
    status: MaterialStatus
    processing_error: Optional[str]
    text_length: Optional[int]
    chunk_count: int
    chroma_collection_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class TeachingMaterialListResponse(BaseModel):
    """Schema for paginated list of materials"""
    materials: List[TeachingMaterialResponse]
    total: int
    page: int
    page_size: int


class MaterialUploadResponse(BaseModel):
    """Schema for upload response"""
    material_id: int
    filename: str
    original_filename: str
    file_size: int
    status: MaterialStatus
    message: str


# ============================================================
# MATERIAL CHUNK SCHEMAS
# ============================================================

class MaterialChunkResponse(BaseModel):
    """Schema for material chunk response"""
    id: int
    material_id: int
    chunk_index: int
    chunk_text: str
    chunk_size: int
    page_number: Optional[int]
    section_title: Optional[str]
    chroma_id: Optional[str]

    class Config:
        from_attributes = True


# ============================================================
# AI TUTOR WITH MATERIAL SCHEMAS
# ============================================================

class AITutorQueryRequest(BaseModel):
    """Schema for AI tutor query with optional material"""
    topic: str = Field(..., min_length=1, max_length=500, description="Topic to learn/teach")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject")
    grade: str = Field(..., min_length=1, max_length=100, description="Grade level")
    board: str = Field(default="CBSE", max_length=100, description="Education board")

    # Optional material selection
    use_uploaded_material: bool = Field(default=False, description="Whether to use uploaded material")
    material_id: Optional[int] = Field(None, description="ID of uploaded material to use")

    @validator('material_id')
    def validate_material_id(cls, v, values):
        """Ensure material_id is provided when use_uploaded_material is True"""
        if values.get('use_uploaded_material') and not v:
            raise ValueError("material_id must be provided when use_uploaded_material is True")
        return v


class AITutorResponse(BaseModel):
    """Schema for AI tutor response"""
    response: str
    source_type: str  # 'curriculum' or 'uploaded_material'
    material_filename: Optional[str] = None
    page_references: Optional[List[int]] = None


# ============================================================
# FILE PROCESSING SCHEMAS
# ============================================================

class FileProcessingStatus(BaseModel):
    """Schema for file processing status"""
    material_id: int
    status: MaterialStatus
    progress: int  # 0-100
    message: str
    error: Optional[str] = None
