-- Migration: Add language column to k12_assessments table
-- Date: 2025-11-05
-- Purpose: Support Hindi and English question generation

-- Add language column with default value
ALTER TABLE k12_assessments
ADD COLUMN IF NOT EXISTS language VARCHAR(20) NOT NULL DEFAULT 'English';

-- Add index for faster filtering
CREATE INDEX IF NOT EXISTS idx_k12_assessments_language ON k12_assessments(language);

-- Add comment
COMMENT ON COLUMN k12_assessments.language IS 'Language for question generation: English or Hindi';

-- Update existing assessments to English (safe default)
UPDATE k12_assessments
SET language = 'English'
WHERE language IS NULL OR language = '';

-- Verify migration
SELECT
    COUNT(*) as total_assessments,
    language,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM k12_assessments
GROUP BY language;
