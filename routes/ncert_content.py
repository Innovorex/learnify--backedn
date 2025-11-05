"""
NCERT Textbook Content API Routes
Endpoints for accessing extracted NCERT textbook content
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import (NCERTTextbookContent, NCERTExample, NCERTExercise,
                   NCERTImage, NCERTActivity, NCERTPDFSource)
from typing import List, Optional
from pydantic import BaseModel


router = APIRouter(prefix="/api/ncert", tags=["NCERT Content"])


# ============================================================================
# Response Models
# ============================================================================

class ContentResponse(BaseModel):
    id: int
    grade: int
    subject: str
    chapter_number: Optional[int]
    chapter_name: str
    content_type: str
    content_text: str
    page_start: Optional[int]
    page_end: Optional[int]

    class Config:
        from_attributes = True


class ExampleResponse(BaseModel):
    id: int
    grade: int
    subject: str
    chapter_name: str
    example_number: Optional[str]
    problem_statement: str
    solution_text: str
    page_number: Optional[int]

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: int
    grade: int
    subject: str
    chapter_name: str
    exercise_number: Optional[str]
    question_number: str
    question_text: str
    page_number: Optional[int]

    class Config:
        from_attributes = True


class ImageResponse(BaseModel):
    id: int
    grade: int
    subject: str
    chapter_name: str
    image_type: str
    figure_number: Optional[str]
    caption: Optional[str]
    file_path: str
    page_number: Optional[int]

    class Config:
        from_attributes = True


class PDFSourceResponse(BaseModel):
    id: int
    grade: int
    subject: str
    book_name: str
    extraction_status: str
    total_content_items: int
    total_examples: int
    total_exercises: int
    total_images: int
    total_activities: int

    class Config:
        from_attributes = True


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/status")
async def get_extraction_status(db: Session = Depends(get_db)):
    """Get overall extraction status for all grades and subjects"""

    sources = db.query(NCERTPDFSource).all()

    summary = {
        "total_books": len(sources),
        "completed": len([s for s in sources if s.extraction_status == "completed"]),
        "in_progress": len([s for s in sources if s.extraction_status == "extracting"]),
        "pending": len([s for s in sources if s.extraction_status == "pending"]),
        "failed": len([s for s in sources if s.extraction_status == "failed"]),
        "books": [PDFSourceResponse.from_orm(s) for s in sources]
    }

    return summary


@router.get("/content/{grade}/{subject}")
async def get_subject_content(
    grade: int,
    subject: str,
    db: Session = Depends(get_db)
):
    """Get all content for a specific grade and subject"""

    content = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.grade == grade,
        NCERTTextbookContent.subject == subject
    ).order_by(NCERTTextbookContent.chapter_number).all()

    if not content:
        raise HTTPException(status_code=404, detail="No content found")

    return {
        "grade": grade,
        "subject": subject,
        "total_chapters": len(content),
        "content": [ContentResponse.from_orm(c) for c in content]
    }


@router.get("/content/{grade}/{subject}/chapter/{chapter_number}")
async def get_chapter_content(
    grade: int,
    subject: str,
    chapter_number: int,
    db: Session = Depends(get_db)
):
    """Get complete content for a specific chapter"""

    # Main content
    content = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.grade == grade,
        NCERTTextbookContent.subject == subject,
        NCERTTextbookContent.chapter_number == chapter_number
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Examples
    examples = db.query(NCERTExample).filter(
        NCERTExample.grade == grade,
        NCERTExample.subject == subject,
        NCERTExample.chapter_name == content.chapter_name
    ).all()

    # Exercises
    exercises = db.query(NCERTExercise).filter(
        NCERTExercise.grade == grade,
        NCERTExercise.subject == subject,
        NCERTExercise.chapter_name == content.chapter_name
    ).all()

    # Images
    images = db.query(NCERTImage).filter(
        NCERTImage.grade == grade,
        NCERTImage.subject == subject,
        NCERTImage.chapter_name == content.chapter_name
    ).all()

    return {
        "chapter_number": chapter_number,
        "chapter_name": content.chapter_name,
        "content": ContentResponse.from_orm(content),
        "examples": [ExampleResponse.from_orm(e) for e in examples],
        "exercises": [ExerciseResponse.from_orm(e) for e in exercises],
        "images": [ImageResponse.from_orm(i) for i in images],
        "stats": {
            "examples_count": len(examples),
            "exercises_count": len(exercises),
            "images_count": len(images)
        }
    }


@router.get("/examples/{grade}/{subject}")
async def get_subject_examples(
    grade: int,
    subject: str,
    chapter_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all examples for a subject (optionally filtered by chapter)"""

    query = db.query(NCERTExample).filter(
        NCERTExample.grade == grade,
        NCERTExample.subject == subject
    )

    if chapter_name:
        query = query.filter(NCERTExample.chapter_name.ilike(f"%{chapter_name}%"))

    examples = query.all()

    if not examples:
        raise HTTPException(status_code=404, detail="No examples found")

    return {
        "grade": grade,
        "subject": subject,
        "chapter_name": chapter_name,
        "total_examples": len(examples),
        "examples": [ExampleResponse.from_orm(e) for e in examples]
    }


@router.get("/exercises/{grade}/{subject}")
async def get_subject_exercises(
    grade: int,
    subject: str,
    chapter_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all exercises for a subject (optionally filtered by chapter)"""

    query = db.query(NCERTExercise).filter(
        NCERTExercise.grade == grade,
        NCERTExercise.subject == subject
    )

    if chapter_name:
        query = query.filter(NCERTExercise.chapter_name.ilike(f"%{chapter_name}%"))

    exercises = query.all()

    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found")

    return {
        "grade": grade,
        "subject": subject,
        "chapter_name": chapter_name,
        "total_exercises": len(exercises),
        "exercises": [ExerciseResponse.from_orm(e) for e in exercises]
    }


@router.get("/search")
async def search_content(
    q: str = Query(..., min_length=3, description="Search query"),
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    content_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search across all NCERT content"""

    # Search in content text
    query = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.content_text.ilike(f"%{q}%")
    )

    if grade:
        query = query.filter(NCERTTextbookContent.grade == grade)
    if subject:
        query = query.filter(NCERTTextbookContent.subject.ilike(f"%{subject}%"))
    if content_type:
        query = query.filter(NCERTTextbookContent.content_type == content_type)

    results = query.limit(50).all()

    return {
        "query": q,
        "filters": {"grade": grade, "subject": subject, "content_type": content_type},
        "total_results": len(results),
        "results": [ContentResponse.from_orm(r) for r in results]
    }


@router.get("/chapters/{grade}/{subject}")
async def list_chapters(
    grade: int,
    subject: str,
    db: Session = Depends(get_db)
):
    """List all chapters for a grade-subject combination"""

    chapters = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.grade == grade,
        NCERTTextbookContent.subject == subject
    ).order_by(NCERTTextbookContent.chapter_number).all()

    if not chapters:
        raise HTTPException(status_code=404, detail="No chapters found")

    return {
        "grade": grade,
        "subject": subject,
        "total_chapters": len(chapters),
        "chapters": [
            {
                "chapter_number": c.chapter_number,
                "chapter_name": c.chapter_name,
                "page_start": c.page_start,
                "page_end": c.page_end
            }
            for c in chapters
        ]
    }


@router.get("/images/{grade}/{subject}")
async def get_subject_images(
    grade: int,
    subject: str,
    chapter_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all images/diagrams for a subject"""

    query = db.query(NCERTImage).filter(
        NCERTImage.grade == grade,
        NCERTImage.subject == subject
    )

    if chapter_name:
        query = query.filter(NCERTImage.chapter_name.ilike(f"%{chapter_name}%"))

    images = query.all()

    if not images:
        raise HTTPException(status_code=404, detail="No images found")

    return {
        "grade": grade,
        "subject": subject,
        "total_images": len(images),
        "images": [ImageResponse.from_orm(i) for i in images]
    }
