-- =====================================================
-- BOARD-BASED FILTERING: Database Migration
-- =====================================================
-- Purpose: Add board column to k12_assessments table
--          and populate with teacher's board
-- Date: 2025-11-11
-- =====================================================

-- Step 1: Add board column if not exists
-- -------------------------------------------------------
ALTER TABLE k12_assessments
ADD COLUMN IF NOT EXISTS board VARCHAR(50);

COMMENT ON COLUMN k12_assessments.board IS 'Board affiliation: CBSE, TELANGANA, ICSE, etc.';

-- Step 2: Populate board from teacher profiles
-- -------------------------------------------------------
-- Maps teacher's board to standardized database values:
-- - "State", "State Board", "Telangana" → "TELANGANA"
-- - "CBSE" → "CBSE"
-- - Default → "CBSE"
UPDATE k12_assessments a
SET board = (
    SELECT CASE
        WHEN LOWER(tp.board) LIKE '%state%'
          OR LOWER(tp.board) LIKE '%telangana%'
          OR LOWER(tp.board) LIKE '%scert%'
          THEN 'TELANGANA'
        WHEN LOWER(tp.board) LIKE '%cbse%'
          THEN 'CBSE'
        WHEN LOWER(tp.board) LIKE '%icse%'
          THEN 'ICSE'
        ELSE 'CBSE'
    END
    FROM teacher_profiles tp
    WHERE tp.user_id = a.teacher_id
)
WHERE board IS NULL;

-- Step 3: Set default CBSE for any remaining NULL values
-- -------------------------------------------------------
UPDATE k12_assessments
SET board = 'CBSE'
WHERE board IS NULL;

-- Step 4: Verify migration
-- -------------------------------------------------------
SELECT
    board,
    COUNT(*) as assessment_count,
    COUNT(DISTINCT teacher_id) as unique_teachers
FROM k12_assessments
GROUP BY board
ORDER BY board;

-- Expected output example:
-- board      | assessment_count | unique_teachers
-- -----------+------------------+----------------
-- CBSE       | 150              | 25
-- TELANGANA  | 45               | 8

-- Step 5: Check sample assessments
-- -------------------------------------------------------
SELECT
    a.id,
    a.teacher_id,
    a.subject,
    a.chapter,
    a.board,
    tp.board as teacher_board_raw
FROM k12_assessments a
LEFT JOIN teacher_profiles tp ON tp.user_id = a.teacher_id
ORDER BY a.id DESC
LIMIT 10;

-- Step 6: Validate no NULL boards remain
-- -------------------------------------------------------
SELECT COUNT(*) as null_board_count
FROM k12_assessments
WHERE board IS NULL;

-- Expected: 0 rows with NULL board

-- =====================================================
-- ROLLBACK (if needed)
-- =====================================================
-- To rollback this migration:
-- ALTER TABLE k12_assessments DROP COLUMN IF EXISTS board;
