-- Progress Analytics - Final Working Version
DROP MATERIALIZED VIEW IF EXISTS teacher_current_scores CASCADE;

CREATE MATERIALIZED VIEW teacher_current_scores AS
WITH
cpd_scores AS (
    SELECT
        p.teacher_id,
        AVG(CASE WHEN m.assessment_type = 'mcq' THEN p.score END) as mcq_avg,
        AVG(CASE WHEN m.assessment_type = 'submission' THEN p.score END) as submission_avg,
        AVG(CASE WHEN m.assessment_type = 'outcome' THEN p.score END) as outcome_avg,
        COUNT(DISTINCT m.id) as modules_assessed
    FROM performance p
    JOIN modules m ON p.module_id = m.id
    WHERE p.created_at >= NOW() - INTERVAL '6 months'
    GROUP BY p.teacher_id
),
career_scores AS (
    SELECT
        tce.teacher_id,
        cc.total_modules,
        COUNT(CASE WHEN mp.passed = TRUE THEN 1 END) as completed_modules,
        AVG(CASE WHEN mp.passed = TRUE THEN mp.exam_score END) as avg_exam_score
    FROM teacher_career_enrollments tce
    JOIN career_courses cc ON tce.course_id = cc.id
    LEFT JOIN module_progress mp ON tce.id = mp.enrollment_id
    WHERE tce.status = 'in_progress'
    GROUP BY tce.teacher_id, cc.total_modules
),
student_scores AS (
    SELECT
        ka.teacher_id,
        COUNT(DISTINCT ka.id) as assessments_created,
        COUNT(DISTINCT kr.student_id) as students_assessed,
        AVG(CASE WHEN (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id) > 0 
            THEN kr.score * 100.0 / (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id)
            ELSE 0 END) as avg_student_score
    FROM k12_assessments ka
    LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
    WHERE ka.created_at >= DATE_TRUNC('month', NOW())
    GROUP BY ka.teacher_id
),
engagement_scores AS (
    SELECT
        teacher_id,
        COUNT(DISTINCT DATE(created_at)) as active_days,
        COUNT(*) as actions_completed
    FROM performance
    WHERE created_at >= DATE_TRUNC('month', NOW())
    GROUP BY teacher_id
),
materials_scores AS (
    SELECT
        teacher_id,
        COUNT(*) as materials_count
    FROM teaching_materials
    WHERE created_at >= DATE_TRUNC('month', NOW())
    GROUP BY teacher_id
)
SELECT
    u.id as teacher_id,
    u.name as teacher_name,
    u.email,
    -- Component Scores
    ROUND(COALESCE((COALESCE(cpd.mcq_avg, 0) * 0.40 + COALESCE(cpd.submission_avg, 0) * 0.35 + COALESCE(cpd.outcome_avg, 0) * 0.25), 0), 1) as cpd_score,
    ROUND(COALESCE(((car.completed_modules * 1.0 / NULLIF(car.total_modules, 0)) * 70 + COALESCE(car.avg_exam_score, 0) * 0.30), 0), 1) as career_score,
    ROUND(COALESCE(LEAST(100, COALESCE(stu.avg_student_score, 0) * 0.60 + (LEAST(stu.assessments_created, 20) / 20.0 * 100 * 0.40)), 0), 1) as student_impact_score,
    ROUND(COALESCE((eng.active_days * 1.0 / 30 * 100), 0), 1) as engagement_score,
    ROUND(COALESCE((LEAST(mat.materials_count, 15) / 15.0 * 100), 0), 1) as materials_score,
    -- Overall Score
    ROUND(COALESCE(
        (COALESCE((COALESCE(cpd.mcq_avg, 0) * 0.40 + COALESCE(cpd.submission_avg, 0) * 0.35 + COALESCE(cpd.outcome_avg, 0) * 0.25), 0) * 0.35) +
        (COALESCE(((car.completed_modules * 1.0 / NULLIF(car.total_modules, 0)) * 70 + COALESCE(car.avg_exam_score, 0) * 0.30), 0) * 0.25) +
        (COALESCE(LEAST(100, COALESCE(stu.avg_student_score, 0) * 0.60 + (LEAST(stu.assessments_created, 20) / 20.0 * 100 * 0.40)), 0) * 0.25) +
        (COALESCE((eng.active_days * 1.0 / 30 * 100), 0) * 0.10) +
        (COALESCE((LEAST(mat.materials_count, 15) / 15.0 * 100), 0) * 0.05),
    0), 1) as overall_score,
    -- Supporting Metrics
    cpd.modules_assessed,
    car.completed_modules,
    car.total_modules,
    stu.assessments_created,
    stu.students_assessed,
    eng.active_days,
    mat.materials_count,
    NOW() as calculated_at
FROM users u
LEFT JOIN cpd_scores cpd ON u.id = cpd.teacher_id
LEFT JOIN career_scores car ON u.id = car.teacher_id
LEFT JOIN student_scores stu ON u.id = stu.teacher_id
LEFT JOIN engagement_scores eng ON u.id = eng.teacher_id
LEFT JOIN materials_scores mat ON u.id = mat.teacher_id
WHERE u.role = 'teacher';

CREATE UNIQUE INDEX idx_current_scores_teacher ON teacher_current_scores(teacher_id);
CREATE INDEX idx_current_scores_overall ON teacher_current_scores(overall_score DESC);

-- Helper function
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

-- Initial refresh
REFRESH MATERIALIZED VIEW teacher_current_scores;

-- Show results
SELECT teacher_name, overall_score, cpd_score, career_score, student_impact_score FROM teacher_current_scores;
