-- Migration: Add Teaching Materials Tables
-- Purpose: Support PDF/DOCX upload with vector search for AI tutor and assessments
-- Date: 2025-10-29

-- ============================================================
-- TEACHING MATERIALS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS teaching_materials (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- File Information
    filename VARCHAR(500) NOT NULL,
    original_filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    file_path TEXT NOT NULL,

    -- Content Metadata
    title VARCHAR(500) NOT NULL,
    description TEXT,
    subject VARCHAR(200),
    grade_level VARCHAR(100),
    topics TEXT[],

    -- Processing Status
    status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,

    -- Text Extraction Results
    extracted_text TEXT,
    text_length INTEGER,
    chunk_count INTEGER DEFAULT 0,
    extraction_metadata JSONB,

    -- Vector DB Information
    chroma_collection_name VARCHAR(200),
    embedding_model VARCHAR(200) DEFAULT 'all-MiniLM-L6-v2',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_materials_teacher ON teaching_materials(teacher_id);
CREATE INDEX IF NOT EXISTS idx_materials_status ON teaching_materials(status);
CREATE INDEX IF NOT EXISTS idx_materials_created ON teaching_materials(created_at DESC);

-- ============================================================
-- MATERIAL CHUNKS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS material_chunks (
    id SERIAL PRIMARY KEY,
    material_id INTEGER NOT NULL REFERENCES teaching_materials(id) ON DELETE CASCADE,

    -- Chunk Information
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_size INTEGER NOT NULL,

    -- Context Information
    page_number INTEGER,
    section_title VARCHAR(500),

    -- Vector DB Reference
    chroma_id VARCHAR(200) UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_material_chunk UNIQUE(material_id, chunk_index)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_chunks_material ON material_chunks(material_id);
CREATE INDEX IF NOT EXISTS idx_chunks_chroma ON material_chunks(chroma_id);

-- ============================================================
-- UPDATE TRIGGER FOR teaching_materials
-- ============================================================
CREATE OR REPLACE FUNCTION update_teaching_materials_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_teaching_materials_timestamp
BEFORE UPDATE ON teaching_materials
FOR EACH ROW
EXECUTE FUNCTION update_teaching_materials_timestamp();

-- ============================================================
-- ROLLBACK SCRIPT (run this to undo migration)
-- ============================================================
-- DROP TRIGGER IF EXISTS trigger_update_teaching_materials_timestamp ON teaching_materials;
-- DROP FUNCTION IF EXISTS update_teaching_materials_timestamp();
-- DROP TABLE IF EXISTS material_chunks;
-- DROP TABLE IF EXISTS teaching_materials;
