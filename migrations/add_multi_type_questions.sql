-- Migration: Add Multi-Type Question Support to K12 Questions
-- Date: 2025-11-05
-- Purpose: Add support for multiple question types beyond MCQ

-- Add new columns to k12_questions table
ALTER TABLE k12_questions
ADD COLUMN IF NOT EXISTS question_type VARCHAR(30) DEFAULT 'multiple_choice' NOT NULL,
ADD COLUMN IF NOT EXISTS question_data JSON,
ADD COLUMN IF NOT EXISTS marks INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS explanation TEXT,
ADD COLUMN IF NOT EXISTS ncert_grade INTEGER,
ADD COLUMN IF NOT EXISTS ncert_subject VARCHAR(100),
ADD COLUMN IF NOT EXISTS ncert_chapter VARCHAR(200),
ADD COLUMN IF NOT EXISTS ncert_topic VARCHAR(200),
ADD COLUMN IF NOT EXISTS concept_tested VARCHAR(200),
ADD COLUMN IF NOT EXISTS blooms_level VARCHAR(20),
ADD COLUMN IF NOT EXISTS cognitive_skill VARCHAR(50);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_k12_questions_type ON k12_questions(question_type);
CREATE INDEX IF NOT EXISTS idx_k12_questions_ncert_grade ON k12_questions(ncert_grade);
CREATE INDEX IF NOT EXISTS idx_k12_questions_ncert_subject ON k12_questions(ncert_subject);
CREATE INDEX IF NOT EXISTS idx_k12_questions_ncert_chapter ON k12_questions(ncert_chapter);

-- Make old columns nullable for backward compatibility
ALTER TABLE k12_questions
ALTER COLUMN options DROP NOT NULL,
ALTER COLUMN correct_answer DROP NOT NULL;

-- Migrate existing MCQ data to new format
UPDATE k12_questions
SET
    question_type = 'multiple_choice',
    question_data = jsonb_build_object(
        'options', options,
        'correct_answer', correct_answer
    )
WHERE question_data IS NULL AND options IS NOT NULL;

-- Add comment to table
COMMENT ON TABLE k12_questions IS 'K-12 assessment questions supporting multiple types: MCQ, True/False, Short Answer, Fill Blank, Multi-Select, Ordering';
COMMENT ON COLUMN k12_questions.question_type IS 'Type of question: multiple_choice, multi_select, true_false, short_answer, fill_blank, ordering';
COMMENT ON COLUMN k12_questions.question_data IS 'Type-specific data in JSON format. Structure varies by question_type';
COMMENT ON COLUMN k12_questions.options IS 'DEPRECATED: Legacy MCQ options. Use question_data instead';
COMMENT ON COLUMN k12_questions.correct_answer IS 'DEPRECATED: Legacy MCQ answer. Use question_data instead';
