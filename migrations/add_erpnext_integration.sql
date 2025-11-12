-- ==========================================
-- ERPNext Integration Migration
-- Date: 2025-11-11
-- Description: Add tables for ERPNext integration
-- ==========================================

-- 1. ERPNext User Mapping Table
-- Tracks mapping between local users and ERPNext entities
CREATE TABLE IF NOT EXISTS erpnext_user_mapping (
    id SERIAL PRIMARY KEY,
    local_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- ERPNext identifiers
    erpnext_user_email VARCHAR(200) UNIQUE NOT NULL,
    erpnext_employee_id VARCHAR(100),
    erpnext_instructor_name VARCHAR(200),

    -- Cached ERPNext data (full JSON for reference)
    erpnext_user_data JSONB,
    erpnext_employee_data JSONB,
    erpnext_instructor_data JSONB,

    -- Sync metadata
    last_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status VARCHAR(20) DEFAULT 'active',
    sync_error TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_erpnext_user_email ON erpnext_user_mapping(erpnext_user_email);
CREATE INDEX IF NOT EXISTS idx_erpnext_local_user ON erpnext_user_mapping(local_user_id);

-- 2. ERPNext Teacher Classes Table
-- Tracks teacher class assignments from Student Groups
CREATE TABLE IF NOT EXISTS erpnext_teacher_classes (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- From Student Group
    student_group_name VARCHAR(100) NOT NULL,
    program VARCHAR(50),
    batch VARCHAR(10),

    -- Parsed values
    grade VARCHAR(10),
    section VARCHAR(5),

    -- From Course Schedule
    subject VARCHAR(100),
    course_schedule_id VARCHAR(100),

    -- Academic info
    academic_year VARCHAR(50),
    academic_term VARCHAR(50),

    -- Full data cache
    student_group_data JSONB,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    -- Sync
    last_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(teacher_id, student_group_name, subject, academic_year)
);

CREATE INDEX IF NOT EXISTS idx_teacher_classes_teacher ON erpnext_teacher_classes(teacher_id);
CREATE INDEX IF NOT EXISTS idx_teacher_classes_grade ON erpnext_teacher_classes(grade, section);
CREATE INDEX IF NOT EXISTS idx_teacher_classes_lookup ON erpnext_teacher_classes(teacher_id, grade, section, subject);

-- 3. ERPNext Student Mapping Table
-- Tracks students from ERPNext
CREATE TABLE IF NOT EXISTS erpnext_student_mapping (
    id SERIAL PRIMARY KEY,
    local_student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- ERPNext identifiers
    erpnext_student_id VARCHAR(100) UNIQUE NOT NULL,
    erpnext_student_name VARCHAR(200),
    erpnext_student_email VARCHAR(200),

    -- Cached data
    erpnext_student_data JSONB,

    -- Current class
    current_grade VARCHAR(10),
    current_section VARCHAR(5),
    roll_number INTEGER,

    -- Sync
    last_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status VARCHAR(20) DEFAULT 'active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_erpnext_student_id ON erpnext_student_mapping(erpnext_student_id);
CREATE INDEX IF NOT EXISTS idx_erpnext_student_local_user ON erpnext_student_mapping(local_student_id);
CREATE INDEX IF NOT EXISTS idx_erpnext_student_class ON erpnext_student_mapping(current_grade, current_section);

-- 4. ERPNext Sync Log Table
-- Audit log for all sync operations
CREATE TABLE IF NOT EXISTS erpnext_sync_logs (
    id SERIAL PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50),
    entity_id VARCHAR(200),

    operation VARCHAR(20),
    status VARCHAR(20) NOT NULL,

    records_processed INTEGER DEFAULT 0,
    records_created INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,

    error_message TEXT,
    execution_time_ms INTEGER,

    triggered_by VARCHAR(50),
    triggered_by_user_id INTEGER REFERENCES users(id),

    sync_started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_completed_at TIMESTAMP,
    duration_seconds DECIMAL(10, 2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sync_log_type ON erpnext_sync_logs(sync_type, created_at);
CREATE INDEX IF NOT EXISTS idx_sync_log_status ON erpnext_sync_logs(status);
CREATE INDEX IF NOT EXISTS idx_sync_log_started ON erpnext_sync_logs(sync_started_at DESC);

-- 5. Update existing users table (add ERPNext tracking columns)
ALTER TABLE users ADD COLUMN IF NOT EXISTS erpnext_synced BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS erpnext_last_sync TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS erpnext_entity_id VARCHAR(100);

-- 6. Update existing teacher_profiles table (add ERPNext info)
ALTER TABLE teacher_profiles ADD COLUMN IF NOT EXISTS erpnext_employee_id VARCHAR(100);
ALTER TABLE teacher_profiles ADD COLUMN IF NOT EXISTS erpnext_instructor_name VARCHAR(200);
ALTER TABLE teacher_profiles ADD COLUMN IF NOT EXISTS auto_synced_from_erpnext BOOLEAN DEFAULT FALSE;

-- Add index for faster ERPNext lookups
CREATE INDEX IF NOT EXISTS idx_users_erpnext_sync ON users(erpnext_last_sync) WHERE erpnext_synced = TRUE;
CREATE INDEX IF NOT EXISTS idx_users_erpnext_entity ON users(erpnext_entity_id) WHERE erpnext_entity_id IS NOT NULL;

-- ==========================================
-- Migration Complete
-- ==========================================
