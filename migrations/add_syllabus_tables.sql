-- ============================================================================
-- MIGRATION: Add CBSE Syllabus Tables (from LS)
-- Date: 2025-10-28
-- Description: Creates syllabus tables for CBSE curriculum data
-- ============================================================================

-- 1. Curriculum Catalog (CBSE syllabus URLs)
CREATE TABLE IF NOT EXISTS curriculum_catalog (
    id SERIAL PRIMARY KEY,
    academic_year VARCHAR(20) NOT NULL,
    stage VARCHAR(20) NOT NULL,
    subject_display_name VARCHAR(200) NOT NULL,
    subject_code VARCHAR(10),
    pdf_url TEXT NOT NULL,
    pdf_filename VARCHAR(300),
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_verified TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_curriculum_catalog_year_stage
    ON curriculum_catalog(academic_year, stage);
CREATE INDEX IF NOT EXISTS idx_curriculum_catalog_subject
    ON curriculum_catalog(subject_display_name);

COMMENT ON TABLE curriculum_catalog IS 'CBSE syllabus catalog with PDF URLs';


-- 2. Syllabus Master (parsed syllabus content)
CREATE TABLE IF NOT EXISTS syllabus_master (
    id SERIAL PRIMARY KEY,
    board VARCHAR(50) DEFAULT 'CBSE',
    class_name VARCHAR(10) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    subject_code VARCHAR(10),
    stage VARCHAR(20),
    academic_year VARCHAR(20) NOT NULL,
    pdf_url TEXT,
    content_extracted TEXT,
    content_sha256 VARCHAR(64),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    catalog_id INTEGER REFERENCES curriculum_catalog(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_syllabus_master_class_subject
    ON syllabus_master(class_name, subject);
CREATE INDEX IF NOT EXISTS idx_syllabus_master_board
    ON syllabus_master(board);
CREATE INDEX IF NOT EXISTS idx_syllabus_master_year
    ON syllabus_master(academic_year);

COMMENT ON TABLE syllabus_master IS 'Master syllabus data with extracted content';


-- 3. Syllabus Topics (chapter-wise breakdown)
CREATE TABLE IF NOT EXISTS syllabus_topics (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES syllabus_master(id) ON DELETE CASCADE,
    chapter_number INTEGER,
    chapter_name TEXT,
    topics JSONB,
    learning_outcomes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_syllabus_topics_syllabus
    ON syllabus_topics(syllabus_id);
CREATE INDEX IF NOT EXISTS idx_syllabus_topics_chapter
    ON syllabus_topics(chapter_number);

COMMENT ON TABLE syllabus_topics IS 'Chapter-wise syllabus topics and learning outcomes';


-- 4. Syllabus Content (full content storage)
CREATE TABLE IF NOT EXISTS syllabus_content (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES syllabus_master(id) ON DELETE CASCADE,
    content_type VARCHAR(50),
    content_text TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(syllabus_id)
);

COMMENT ON TABLE syllabus_content IS 'Full syllabus content storage';


-- 5. Syllabus Fetch Log (tracking syllabus fetches)
CREATE TABLE IF NOT EXISTS syllabus_fetch_log (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(10),
    subject VARCHAR(100),
    board VARCHAR(50),
    status VARCHAR(50),
    error_message TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fetch_log_class_subject
    ON syllabus_fetch_log(class_name, subject);
CREATE INDEX IF NOT EXISTS idx_fetch_log_status
    ON syllabus_fetch_log(status);

COMMENT ON TABLE syllabus_fetch_log IS 'Log of syllabus fetch operations';


-- Verification
DO $$
BEGIN
    RAISE NOTICE '✅ Syllabus tables created successfully!';
    RAISE NOTICE 'Created: curriculum_catalog';
    RAISE NOTICE 'Created: syllabus_master';
    RAISE NOTICE 'Created: syllabus_topics';
    RAISE NOTICE 'Created: syllabus_content';
    RAISE NOTICE 'Created: syllabus_fetch_log';
END $$;
