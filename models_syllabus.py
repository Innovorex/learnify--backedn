"""
Syllabus Models for CBSE Curriculum Management
==============================================
SQLAlchemy models for syllabus data migrated from LS database.
These models match the schema imported from ai_assessment database.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    JSON, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import JSONB
from database import Base
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def ist_now():
    """Return current time in IST"""
    return datetime.now(IST)


class CurriculumCatalog(Base):
    """
    Dynamic catalog of CBSE syllabus URLs (year-aware)
    Automatically discovered from CBSE website
    """
    __tablename__ = "curriculum_catalog"

    id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(String(20), nullable=False)               # '2024-25', '2025-26'
    stage = Column(String(20), nullable=False)                       # 'secondary', 'sr_secondary'
    subject_display_name = Column(String(200), nullable=False)       # 'Mathematics', 'Science'
    subject_code = Column(String(10))                                # '041', '086', etc.
    pdf_url = Column(Text, nullable=False)                           # Full URL to PDF
    pdf_filename = Column(String(300))                               # Original filename
    discovered_at = Column(DateTime, default=ist_now)
    last_verified = Column(DateTime)                                 # Last time URL was checked
    is_active = Column(Boolean, default=True)


class SyllabusMaster(Base):
    """
    Master table storing complete syllabus content with SHA256 versioning
    Supports both CBSE and State Boards
    """
    __tablename__ = "syllabus_master"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String(50), default="CBSE")
    class_name = Column(String(10), nullable=False)                  # '9', '10', '11', '12'
    subject = Column(String(100), nullable=False)
    subject_code = Column(String(10))                                # CBSE subject code
    stage = Column(String(20))                                       # 'secondary' or 'sr_secondary'
    academic_year = Column(String(20), nullable=False)               # '2024-25'
    pdf_url = Column(Text)
    content_extracted = Column(Text)                                 # Full extracted text
    content_sha256 = Column(String(64))                             # SHA256 checksum for version control
    last_updated = Column(DateTime, default=ist_now)
    is_active = Column(Boolean, default=True)
    catalog_id = Column(Integer, ForeignKey("curriculum_catalog.id"))  # Link to catalog entry

    # State Board Support
    board_type = Column(String(20), default='CBSE')                  # 'CBSE' or 'STATE'
    state_board_id = Column(Integer)                                 # Reference to state_boards
    medium = Column(String(20), default='English')                   # 'English', 'Telugu', 'Hindi', etc.
    textbook_name = Column(String(200))                              # State board specific textbook name
    publisher = Column(String(100))                                  # e.g., 'SCERT Telangana', 'SCERT AP'

    # Three Language Formula Support
    language_position = Column(String(20))                           # 'FL' (First), 'SL' (Second), 'TL' (Third), or NULL


class SyllabusTopics(Base):
    """
    Hierarchical topic structure with parent-child relationships
    """
    __tablename__ = "syllabus_topics"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus_master.id", ondelete="CASCADE"), nullable=False)

    # Hierarchy fields
    parent_topic_id = Column(Integer, ForeignKey("syllabus_topics.id"))  # For nested topics
    is_chapter = Column(Boolean, default=True)                           # Distinguish chapters from subtopics

    # Structure fields
    unit_number = Column(Integer)                                    # Unit 1, 2, 3...
    unit_name = Column(String(200))                                  # "Chemical Reactions"
    chapter_number = Column(Integer)                                 # Chapter 1, 2, 3...
    chapter_name = Column(String(200), nullable=False)               # "Real Numbers"
    topic_name = Column(String(300))                                 # "Euclid's Division Lemma"

    # Content arrays (JSON)
    subtopics = Column(JSONB)                                        # ["HCF", "LCM", ...]
    learning_outcomes = Column(JSONB)                                # ["Understand Euclid's algorithm", ...]
    key_concepts = Column(JSONB)                                     # ["Prime numbers", "Divisibility", ...]
    content_details = Column(Text)                                   # Long-form explanations

    # Metadata
    weightage = Column(Integer)                                      # Marks weightage in exam
    difficulty_level = Column(String(20), default='medium')          # easy/medium/hard
    sequence_order = Column(Integer)                                 # Display order
    created_at = Column(DateTime, default=ist_now)
    updated_at = Column(DateTime, default=ist_now, onupdate=ist_now)


class SyllabusContent(Base):
    """
    Full syllabus content storage for quick retrieval
    """
    __tablename__ = "syllabus_content"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    chapter = Column(String, nullable=False)
    full_content = Column(Text, nullable=False)                      # Complete chapter content
    learning_objectives = Column(JSON)                               # Learning objectives
    key_concepts = Column(JSON)                                      # Key concepts
    topics = Column(JSON)                                            # Topics list
    source_url = Column(String)                                      # Source URL
    content_hash = Column(String)                                    # Hash for version control
    pdf_path = Column(String)                                        # Local PDF path
    fetched_at = Column(DateTime)                                    # When fetched
    last_used_at = Column(DateTime)                                  # Last accessed
    times_used = Column(Integer)                                     # Usage counter


class SyllabusFetchLog(Base):
    """
    Log of all syllabus fetch operations
    """
    __tablename__ = "syllabus_fetch_log"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String(50))
    class_name = Column(String(10))
    subject = Column(String(100))
    academic_year = Column(String(20))
    fetch_status = Column(String(50))                                # 'pending', 'success', 'failed'
    source = Column(String(200))                                     # URL or source identifier
    http_status = Column(Integer)                                    # HTTP response code
    attempt = Column(Integer, default=1)                             # Retry attempt number
    duration_ms = Column(Integer)                                    # Request duration in ms
    error_message = Column(Text)                                     # Error details if failed
    error_type = Column(String(100))                                 # Exception type
    fetched_at = Column(DateTime, default=ist_now)
    completed_at = Column(DateTime)
