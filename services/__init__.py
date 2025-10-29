"""
Services Package for K-12 Assessment System
==========================================
AI-powered question generation and syllabus management services.
"""

from .ai_question_generator import generate_questions, generate_sample_questions
from .syllabus_service import SyllabusService, get_syllabus_service
from .syllabus_scraper import CBSESyllabusDiscovery, get_catalog_entry

__all__ = [
    'generate_questions',
    'generate_sample_questions',
    'SyllabusService',
    'get_syllabus_service',
    'CBSESyllabusDiscovery',
    'get_catalog_entry'
]
