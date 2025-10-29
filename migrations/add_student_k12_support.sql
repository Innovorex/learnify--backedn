-- ============================================================================
-- MIGRATION: Add Student Role and K-12 Assessment Support
-- Date: 2025-10-27
-- Description: Adds student role to users table and creates K-12 assessment
--              tables for the student assessment system
-- ============================================================================

-- Step 1: Add student-specific fields to users table
-- ============================================================================
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS class_name VARCHAR(10),
  ADD COLUMN IF NOT EXISTS section VARCHAR(5);

COMMENT ON COLUMN users.class_name IS 'Student class/grade (e.g., "9", "10", "11")';
COMMENT ON COLUMN users.section IS 'Student section (e.g., "A", "B", "C")';

-- Create index for student queries
CREATE INDEX IF NOT EXISTS idx_users_class_section
  ON users(class_name, section);


-- Step 2: Create K-12 Assessment Tables
-- ============================================================================

-- K-12 Assessments (created by teachers for students)
CREATE TABLE IF NOT EXISTS k12_assessments (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Target students
    class_name VARCHAR(10) NOT NULL,
    section VARCHAR(5) NOT NULL,

    -- Assessment details
    subject VARCHAR(100) NOT NULL,
    chapter VARCHAR(200) NOT NULL,

    -- Timing
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_k12_assessments_teacher
  ON k12_assessments(teacher_id);
CREATE INDEX IF NOT EXISTS idx_k12_assessments_class
  ON k12_assessments(class_name, section);
CREATE INDEX IF NOT EXISTS idx_k12_assessments_timing
  ON k12_assessments(start_time, end_time);

COMMENT ON TABLE k12_assessments IS 'K-12 student assessments created by teachers';


-- K-12 Questions (question bank for assessments)
CREATE TABLE IF NOT EXISTS k12_questions (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES k12_assessments(id) ON DELETE CASCADE,

    question TEXT NOT NULL,
    options JSONB NOT NULL,           -- {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer VARCHAR(5) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'medium',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_k12_questions_assessment
  ON k12_questions(assessment_id);

COMMENT ON TABLE k12_questions IS 'Question bank for K-12 assessments';


-- K-12 Results (student exam submissions)
CREATE TABLE IF NOT EXISTS k12_results (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_id INTEGER NOT NULL REFERENCES k12_assessments(id) ON DELETE CASCADE,

    answers JSONB,                    -- {question_id: selected_option}
    score INTEGER DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Prevent duplicate submissions
    UNIQUE(student_id, assessment_id)
);

CREATE INDEX IF NOT EXISTS idx_k12_results_student
  ON k12_results(student_id);
CREATE INDEX IF NOT EXISTS idx_k12_results_assessment
  ON k12_results(assessment_id);

COMMENT ON TABLE k12_results IS 'Student exam results and submissions';


-- Step 3: Migration Verification
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE '✅ Migration completed successfully!';
    RAISE NOTICE 'Added student fields to users table';
    RAISE NOTICE 'Created k12_assessments table';
    RAISE NOTICE 'Created k12_questions table';
    RAISE NOTICE 'Created k12_results table';
END $$;
