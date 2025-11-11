-- ═══════════════════════════════════════════════════════════════
-- PROGRESS ANALYTICS V2 - DATABASE SCHEMA (Simplified)
-- Works without daily_growth_actions table
-- ═══════════════════════════════════════════════════════════════

-- ───────────────────────────────────────────────────────────────
-- 1. Teacher Progress Snapshots (Daily aggregation)
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teacher_progress_snapshots (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) DEFAULT 'daily',

    -- Component scores (0-100 each)
    cpd_score FLOAT DEFAULT 0,
    career_score FLOAT DEFAULT 0,
    student_impact_score FLOAT DEFAULT 0,
    engagement_score FLOAT DEFAULT 0,
    materials_score FLOAT DEFAULT 0,

    -- Overall performance score (0-100)
    overall_score FLOAT DEFAULT 0,

    -- Activity metrics
    active_days INTEGER DEFAULT 0,
    actions_completed INTEGER DEFAULT 0,
    time_spent_minutes INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_teacher_snapshot UNIQUE (teacher_id, snapshot_date, period_type)
);

CREATE INDEX IF NOT EXISTS idx_progress_teacher_date ON teacher_progress_snapshots(teacher_id, snapshot_date);
CREATE INDEX IF NOT EXISTS idx_progress_period ON teacher_progress_snapshots(period_type, snapshot_date);


-- ───────────────────────────────────────────────────────────────
-- 2. Materialized View: Current Teacher Scores (Simplified)
-- ───────────────────────────────────────────────────────────────
DROP MATERIALIZED VIEW IF EXISTS teacher_current_scores CASCADE;

CREATE MATERIALIZED VIEW teacher_current_scores AS
WITH
-- CPD Performance Calculation
cpd_scores AS (
    SELECT
        p.teacher_id,
        AVG(CASE WHEN m.assessment_type = 'mcq' THEN p.score END) as mcq_avg,
        AVG(CASE WHEN m.assessment_type = 'submission' THEN p.score END) as submission_avg,
        AVG(CASE WHEN m.assessment_type = 'outcome' THEN p.score END) as outcome_avg,
        COUNT(DISTINCT m.id) as modules_assessed,
        AVG(p.score) as overall_avg
    FROM performance p
    JOIN modules m ON p.module_id = m.id
    WHERE p.created_at >= NOW() - INTERVAL '6 months'
    GROUP BY p.teacher_id
),

-- Career Progress Calculation
career_scores AS (
    SELECT
        tce.teacher_id,
        cc.total_modules,
        COUNT(CASE WHEN mp.passed = TRUE THEN 1 END) as completed_modules,
        AVG(CASE WHEN mp.passed = TRUE THEN mp.exam_score END) as avg_exam_score,
        (COUNT(CASE WHEN mp.passed = TRUE THEN 1 END) * 1.0 / NULLIF(cc.total_modules, 0)) * 100 as progress_pct
    FROM teacher_career_enrollments tce
    JOIN career_courses cc ON tce.course_id = cc.id
    LEFT JOIN module_progress mp ON tce.id = mp.enrollment_id
    WHERE tce.status = 'in_progress'
    GROUP BY tce.teacher_id, cc.total_modules
),

-- Student Impact Calculation
student_scores AS (
    SELECT
        ka.teacher_id,
        COUNT(DISTINCT ka.id) as assessments_created,
        COUNT(DISTINCT kr.student_id) as students_assessed,
        AVG(kr.score * 1.0 / (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id) * 100) as avg_student_score,
        COUNT(DISTINCT kr.student_id) * 1.0 / NULLIF(
            (SELECT COUNT(DISTINCT concat(class_name, section)) FROM k12_assessments WHERE teacher_id = ka.teacher_id), 0
        ) as participation_rate
    FROM k12_assessments ka
    LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
    WHERE ka.created_at >= DATE_TRUNC('month', NOW())
    GROUP BY ka.teacher_id
),

-- Engagement Calculation (using performance table as proxy)
engagement_scores AS (
    SELECT
        teacher_id,
        COUNT(DISTINCT DATE(created_at)) as active_days,
        COUNT(*) as actions_completed
    FROM performance
    WHERE created_at >= DATE_TRUNC('month', NOW())
    GROUP BY teacher_id
),

-- Materials Calculation
materials_scores AS (
    SELECT
        tm.teacher_id,
        COUNT(DISTINCT tm.id) as materials_count,
        COUNT(DISTINCT ats.id) as ai_tutor_uses
    FROM teaching_materials tm
    LEFT JOIN ai_tutor_sessions ats ON tm.teacher_id = ats.user_id
    WHERE tm.created_at >= DATE_TRUNC('month', NOW())
    GROUP BY tm.teacher_id
)

-- Final Score Calculation
SELECT
    u.id as teacher_id,
    u.name as teacher_name,
    u.email,

    -- Component Scores (0-100 each)
    ROUND(COALESCE(
        (COALESCE(cpd.mcq_avg, 0) * 0.40 +
         COALESCE(cpd.submission_avg, 0) * 0.35 +
         COALESCE(cpd.outcome_avg, 0) * 0.25),
        0
    ), 1) as cpd_score,

    ROUND(COALESCE(
        (car.progress_pct * 0.70 + (car.avg_exam_score) * 0.30),
        0
    ), 1) as career_score,

    ROUND(COALESCE(
        LEAST(100,
            (LEAST(stu.avg_student_score, 100) * 0.60) +
            (LEAST(stu.assessments_created, 20) / 20.0 * 100 * 0.30) +
            (COALESCE(stu.participation_rate, 0) * 100 * 0.10)
        ),
        0
    ), 1) as student_impact_score,

    ROUND(COALESCE(
        (eng.active_days * 1.0 / EXTRACT(DAY FROM (DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day'))::DATE * 100 * 0.70) +
        (LEAST(eng.actions_completed, 30) / 30.0 * 100 * 0.30),
        0
    ), 1) as engagement_score,

    ROUND(COALESCE(
        (LEAST(mat.materials_count, 15) / 15.0 * 100 * 0.60) +
        (LEAST(mat.ai_tutor_uses, 30) / 30.0 * 100 * 0.40),
        0
    ), 1) as materials_score,

    -- Overall Score (weighted sum)
    ROUND(
        COALESCE(
            (COALESCE(
                (COALESCE(cpd.mcq_avg, 0) * 0.40 +
                 COALESCE(cpd.submission_avg, 0) * 0.35 +
                 COALESCE(cpd.outcome_avg, 0) * 0.25),
                0
            ) * 0.35) +
            (COALESCE(
                (car.progress_pct * 0.70 + (car.avg_exam_score) * 0.30),
                0
            ) * 0.25) +
            (COALESCE(
                LEAST(100,
                    (LEAST(stu.avg_student_score, 100) * 0.60) +
                    (LEAST(stu.assessments_created, 20) / 20.0 * 100 * 0.30) +
                    (COALESCE(stu.participation_rate, 0) * 100 * 0.10)
                ),
                0
            ) * 0.25) +
            (COALESCE(
                (eng.active_days * 1.0 / EXTRACT(DAY FROM (DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day'))::DATE * 100 * 0.70) +
                (LEAST(eng.actions_completed, 30) / 30.0 * 100 * 0.30),
                0
            ) * 0.10) +
            (COALESCE(
                (LEAST(mat.materials_count, 15) / 15.0 * 100 * 0.60) +
                (LEAST(mat.ai_tutor_uses, 30) / 30.0 * 100 * 0.40),
                0
            ) * 0.05),
            0
        ),
        1
    ) as overall_score,

    -- Supporting Metrics
    cpd.modules_assessed,
    cpd.mcq_avg,
    cpd.submission_avg,
    cpd.outcome_avg,
    car.completed_modules,
    car.total_modules,
    car.avg_exam_score,
    stu.assessments_created,
    stu.students_assessed,
    stu.avg_student_score,
    eng.active_days,
    mat.materials_count,
    mat.ai_tutor_uses,

    -- Timestamp
    NOW() as calculated_at

FROM users u
LEFT JOIN cpd_scores cpd ON u.id = cpd.teacher_id
LEFT JOIN career_scores car ON u.id = car.teacher_id
LEFT JOIN student_scores stu ON u.id = stu.teacher_id
LEFT JOIN engagement_scores eng ON u.id = eng.teacher_id
LEFT JOIN materials_scores mat ON u.id = mat.teacher_id
WHERE u.role = 'teacher';

-- Create indexes on materialized view
CREATE UNIQUE INDEX idx_current_scores_teacher ON teacher_current_scores(teacher_id);
CREATE INDEX idx_current_scores_overall ON teacher_current_scores(overall_score DESC);


-- ───────────────────────────────────────────────────────────────
-- 3. Helper Functions
-- ───────────────────────────────────────────────────────────────

-- Function to get score rating
CREATE OR REPLACE FUNCTION get_score_rating(score FLOAT)
RETURNS VARCHAR(20) AS $$
BEGIN
    IF score >= 90 THEN RETURN 'Excellent';
    ELSIF score >= 80 THEN RETURN 'Very Good';
    ELSIF score >= 70 THEN RETURN 'Good';
    ELSIF score >= 60 THEN RETURN 'Satisfactory';
    ELSE RETURN 'Needs Improvement';
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_teacher_scores()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY teacher_current_scores;
END;
$$ LANGUAGE plpgsql;


-- ───────────────────────────────────────────────────────────────
-- 4. Initial Data Population
-- ───────────────────────────────────────────────────────────────

-- Refresh materialized view immediately
REFRESH MATERIALIZED VIEW teacher_current_scores;

-- Create initial snapshot for all teachers
INSERT INTO teacher_progress_snapshots (
    teacher_id, snapshot_date, period_type,
    cpd_score, career_score, student_impact_score, engagement_score, materials_score, overall_score
)
SELECT
    teacher_id,
    CURRENT_DATE,
    'daily',
    cpd_score,
    career_score,
    student_impact_score,
    engagement_score,
    materials_score,
    overall_score
FROM teacher_current_scores
ON CONFLICT (teacher_id, snapshot_date, period_type) DO UPDATE
SET
    cpd_score = EXCLUDED.cpd_score,
    career_score = EXCLUDED.career_score,
    student_impact_score = EXCLUDED.student_impact_score,
    engagement_score = EXCLUDED.engagement_score,
    materials_score = EXCLUDED.materials_score,
    overall_score = EXCLUDED.overall_score,
    updated_at = NOW();

-- Success message
DO $$
DECLARE
    teacher_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO teacher_count FROM teacher_current_scores;
    RAISE NOTICE '✅ Progress analytics schema created successfully!';
    RAISE NOTICE '✅ Materialized view refreshed with current scores.';
    RAISE NOTICE '✅ Found % teacher(s) with calculated scores.', teacher_count;
    RAISE NOTICE '📊 Run: SELECT * FROM teacher_current_scores; to view results.';
END $$;
