from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, BigInteger, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class TeachingMaterial(Base):
    """
    Model for storing uploaded teaching materials (PDF, DOCX, TXT)
    Each material is processed and stored in its own Chroma collection
    """
    __tablename__ = "teaching_materials"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # File Information
    filename = Column(String(500), nullable=False)  # UUID-based filename
    original_filename = Column(String(500), nullable=False)  # User's original filename
    file_type = Column(String(50), nullable=False)  # 'pdf', 'docx', 'txt'
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    file_path = Column(Text, nullable=False)  # Storage path on disk

    # Content Metadata
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(200), nullable=True)
    grade_level = Column(String(100), nullable=True)
    topics = Column(ARRAY(Text), nullable=True)

    # Processing Status
    status = Column(String(50), default="pending")  # 'pending', 'processing', 'completed', 'failed'
    processing_error = Column(Text, nullable=True)

    # Text Extraction Results
    extracted_text = Column(Text, nullable=True)
    text_length = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0)
    extraction_metadata = Column(JSONB, nullable=True)  # Store page count, etc.

    # Vector DB Information
    chroma_collection_name = Column(String(200), nullable=True)
    embedding_model = Column(String(200), default="all-MiniLM-L6-v2")

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    processed_at = Column(TIMESTAMP, nullable=True)

    # Relationships
    teacher = relationship("User", back_populates="teaching_materials")
    chunks = relationship("MaterialChunk", back_populates="material", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TeachingMaterial(id={self.id}, title='{self.title}', status='{self.status}')>"


class MaterialChunk(Base):
    """
    Individual text chunks from teaching materials for vector search
    Each chunk is embedded and stored in Chroma DB
    """
    __tablename__ = "material_chunks"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("teaching_materials.id", ondelete="CASCADE"), nullable=False, index=True)

    # Chunk Information
    chunk_index = Column(Integer, nullable=False)  # Order in document (0, 1, 2, ...)
    chunk_text = Column(Text, nullable=False)
    chunk_size = Column(Integer, nullable=False)  # Character count

    # Context Information (for PDFs)
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(500), nullable=True)

    # Vector DB Reference
    chroma_id = Column(String(200), unique=True, nullable=True)  # ID in Chroma DB

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    material = relationship("TeachingMaterial", back_populates="chunks")

    def __repr__(self):
        return f"<MaterialChunk(id={self.id}, material_id={self.material_id}, chunk_index={self.chunk_index})>"
