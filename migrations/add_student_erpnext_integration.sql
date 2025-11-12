-- Student ERPNext Integration Migration
-- Adds tables for student profile sync from ERPNext portal

-- =====================================================
-- 1. Student ERPNext Mapping Table
-- =====================================================
CREATE TABLE IF NOT EXISTS erpnext_student_mapping (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    erpnext_student_id VARCHAR(255) NOT NULL UNIQUE,
    student_name VARCHAR(255),
    roll_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_student_mapping_user_id ON erpnext_student_mapping(user_id);
CREATE INDEX IF NOT EXISTS idx_student_mapping_erpnext_id ON erpnext_student_mapping(erpnext_student_id);

-- =====================================================
-- 2. Student Groups (Classes/Sections) Membership
-- =====================================================
CREATE TABLE IF NOT EXISTS erpnext_student_groups (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    student_group_name VARCHAR(100) NOT NULL,
    grade VARCHAR(10) NOT NULL,
    section VARCHAR(10) NOT NULL,
    roll_number INTEGER,
    academic_year VARCHAR(20),
    program VARCHAR(255),
    batch VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, student_group_name, academic_year)
);

CREATE INDEX IF NOT EXISTS idx_student_groups_student_id ON erpnext_student_groups(student_id);
CREATE INDEX IF NOT EXISTS idx_student_groups_grade_section ON erpnext_student_groups(grade, section);
CREATE INDEX IF NOT EXISTS idx_student_groups_academic_year ON erpnext_student_groups(academic_year);

-- =====================================================
-- 3. Add ERPNext Fields to Users Table (if not exists)
-- =====================================================
ALTER TABLE users ADD COLUMN IF NOT EXISTS erpnext_student_id VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS roll_number INTEGER;

CREATE INDEX IF NOT EXISTS idx_users_erpnext_student_id ON users(erpnext_student_id);

-- =====================================================
-- 4. Comments
-- =====================================================
COMMENT ON TABLE erpnext_student_mapping IS 'Maps local users to ERPNext Student DocType';
COMMENT ON TABLE erpnext_student_groups IS 'Stores student class/section membership from ERPNext Student Groups';

COMMENT ON COLUMN erpnext_student_mapping.erpnext_student_id IS 'ERPNext Student ID (e.g., EDU-STU-2024-00001)';
COMMENT ON COLUMN erpnext_student_groups.student_group_name IS 'ERPNext Student Group name (e.g., "10 A")';
COMMENT ON COLUMN erpnext_student_groups.grade IS 'Parsed grade from group name (e.g., "10")';
COMMENT ON COLUMN erpnext_student_groups.section IS 'Parsed section from group name (e.g., "A")';
