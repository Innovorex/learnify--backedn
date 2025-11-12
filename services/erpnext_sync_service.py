"""
ERPNext Synchronization Service
Handles syncing teachers, students, classes from ERPNext to local database
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging
import json

from services.erpnext_client import get_erpnext_client
from models import User, Role
from database import SessionLocal

logger = logging.getLogger(__name__)


class ERPNextSyncService:
    """Service for syncing ERPNext data to local database"""

    def __init__(self, db: Session):
        self.db = db
        self.client = get_erpnext_client()

    async def sync_teacher(self, email: str) -> Dict[str, Any]:
        """
        Sync complete teacher profile from ERPNext

        Flow:
        1. Fetch data from ERPNext (via client)
        2. Create/update local User
        3. Create/update TeacherProfile
        4. Create/update ERPNextUserMapping
        5. Create/update ERPNextTeacherClasses
        6. Log sync operation
        """

        sync_log_id = self._start_sync_log("teacher", email)

        try:
            # Fetch from ERPNext
            erpnext_data = await self.client.sync_teacher_complete(email)

            if not erpnext_data["success"]:
                self._fail_sync_log(sync_log_id, erpnext_data.get("error"))
                return {"success": False, "error": erpnext_data.get("error")}

            # Create/update local user
            user = self._upsert_user(
                email=email,
                name=erpnext_data["user"].get("full_name") or erpnext_data["employee"].get("employee_name"),
                role=Role.teacher
            )

            # Create/update teacher profile
            self._upsert_teacher_profile(
                user_id=user.id,
                employee_data=erpnext_data["employee"],
                board=erpnext_data["board"],
                subjects=erpnext_data["subjects"],
                classes=erpnext_data["classes"],
                instructor_name=erpnext_data["instructor"].get("name") if erpnext_data.get("instructor") else None
            )

            # Save ERPNext mapping
            self._upsert_erpnext_mapping(
                user_id=user.id,
                email=email,
                employee_id=erpnext_data["employee"].get("name"),
                instructor_name=erpnext_data["instructor"].get("name"),
                user_data=erpnext_data["user"],
                employee_data=erpnext_data["employee"],
                instructor_data=erpnext_data["instructor"]
            )

            # Save class assignments
            await self._upsert_teacher_classes(
                user_id=user.id,
                classes=erpnext_data["classes"]
            )

            self.db.commit()
            self._complete_sync_log(sync_log_id, "success", len(erpnext_data["classes"]) + 1)

            return {
                "success": True,
                "user": user,
                "classes": erpnext_data["classes"],
                "board": erpnext_data["board"]
            }

        except Exception as e:
            self.db.rollback()
            self._fail_sync_log(sync_log_id, str(e))
            logger.error(f"Sync failed for {email}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def sync_student(self, email: str) -> Dict[str, Any]:
        """
        Sync individual student profile from ERPNext (called on login)

        Flow:
        1. Fetch student from ERPNext by email
        2. Get student groups (classes) the student belongs to
        3. Create/update local User
        4. Update student mapping
        5. Update student groups
        """
        sync_log_id = self._start_sync_log("student", email)

        try:
            # Fetch student from ERPNext by email
            student_data = await self.client.get_student_by_email(email)

            if not student_data:
                self._fail_sync_log(sync_log_id, "Student not found in ERPNext")
                return {"success": False, "error": "Student not found in ERPNext"}

            student_id = student_data.get("name")  # ERPNext Student ID
            student_name = student_data.get("student_name")

            # Get student groups (classes/sections)
            student_groups = await self.client.get_student_groups_for_student(student_id)

            if not student_groups:
                logger.warning(f"No student groups found for {student_id}")
                # Continue anyway - create user even if no classes

            # Parse first student group for default class/section
            grade = ""
            section = ""
            roll_number = None

            if student_groups:
                first_group = student_groups[0]
                group_name = first_group.get("group_name", "")
                grade, section = self._parse_group_name(group_name)
                roll_number = first_group.get("roll_number")

            # Create/update local user
            user = self._upsert_user(
                email=email,
                name=student_name,
                role=Role.student,
                class_name=grade,
                section=section
            )

            # Save student mapping
            self._upsert_student_mapping(
                user_id=user.id,
                student_id=student_id,
                student_data=student_data,
                grade=grade,
                section=section
            )

            # Save student groups
            await self._upsert_student_groups(
                user_id=user.id,
                groups=student_groups
            )

            self.db.commit()
            self._complete_sync_log(sync_log_id, "success", len(student_groups) + 1)

            return {
                "success": True,
                "user": user,
                "groups": student_groups,
                "message": f"Student profile synced: {student_name}"
            }

        except Exception as e:
            self.db.rollback()
            self._fail_sync_log(sync_log_id, str(e))
            logger.error(f"Student sync failed for {email}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def sync_students_for_class(self, grade: str, section: str) -> Dict[str, Any]:
        """Sync all students in a class from ERPNext"""

        group_name = f"{grade} {section}"
        sync_log_id = self._start_sync_log("students", group_name)

        try:
            # Fetch students from ERPNext
            students = await self.client.get_students_by_group(group_name)

            synced_count = 0
            for student_data in students:
                student_id = student_data.get("name")
                email = student_data.get("student_email_id") or student_data.get("user")

                if not email:
                    email = f"{student_id}@temp.school.com"

                # Create/update student
                user = self._upsert_user(
                    email=email,
                    name=student_data.get("student_name"),
                    role=Role.student,
                    class_name=grade,
                    section=section
                )

                # Save student mapping
                self._upsert_student_mapping(
                    user_id=user.id,
                    student_id=student_id,
                    student_data=student_data,
                    grade=grade,
                    section=section
                )

                synced_count += 1

            self.db.commit()
            self._complete_sync_log(sync_log_id, "success", synced_count)

            return {"success": True, "students_synced": synced_count}

        except Exception as e:
            self.db.rollback()
            self._fail_sync_log(sync_log_id, str(e))
            return {"success": False, "error": str(e)}

    def _upsert_user(
        self,
        email: str,
        name: str,
        role: Role,
        class_name: str = None,
        section: str = None
    ) -> User:
        """Create or update user"""
        user = self.db.query(User).filter(User.email == email.lower()).first()

        if user:
            user.name = name
            user.erpnext_synced = True
            user.erpnext_last_sync = datetime.now()
            if class_name:
                user.class_name = class_name
            if section:
                user.section = section
        else:
            from security import hash_password
            user = User(
                email=email.lower(),
                name=name,
                role=role,
                password_hash=hash_password(f"temp_{email}"),
                class_name=class_name,
                section=section,
                erpnext_synced=True,
                erpnext_last_sync=datetime.now()
            )
            self.db.add(user)
            self.db.flush()  # Get ID

        return user

    def _upsert_teacher_profile(
        self,
        user_id: int,
        employee_data: Dict,
        board: str,
        subjects: List[str],
        classes: List[Dict],
        instructor_name: str = None
    ):
        """Create or update teacher profile"""
        from models import TeacherProfile

        # Extract grades
        grades = self._extract_grades_from_classes(classes)

        # Get qualification
        education_list = employee_data.get("education", [])
        qualification = education_list[0].get("qualification") if education_list else "Not specified"

        profile = self.db.query(TeacherProfile).filter(
            TeacherProfile.user_id == user_id
        ).first()

        if profile:
            # Update existing profile
            profile.education = qualification
            profile.grades_teaching = grades
            profile.subjects_teaching = ", ".join(subjects)
            profile.board = board
            profile.erpnext_employee_id = employee_data.get("name")
            profile.erpnext_instructor_name = instructor_name
            profile.auto_synced_from_erpnext = True
        else:
            # Create new profile
            profile = TeacherProfile(
                user_id=user_id,
                name=employee_data.get("employee_name"),
                education=qualification,
                grades_teaching=grades,
                subjects_teaching=", ".join(subjects),
                experience_years=0,
                board=board,
                state="Telangana",
                erpnext_employee_id=employee_data.get("name"),
                erpnext_instructor_name=instructor_name,
                auto_synced_from_erpnext=True
            )
            self.db.add(profile)

    def _upsert_erpnext_mapping(
        self,
        user_id: int,
        email: str,
        employee_id: str,
        instructor_name: str,
        user_data: Dict,
        employee_data: Dict,
        instructor_data: Dict
    ):
        """Save ERPNext user mapping"""
        self.db.execute(
            text("""
                INSERT INTO erpnext_user_mapping
                    (local_user_id, erpnext_user_email, erpnext_employee_id, erpnext_instructor_name,
                     erpnext_user_data, erpnext_employee_data, erpnext_instructor_data, last_synced_at)
                VALUES
                    (:user_id, :email, :employee_id, :instructor_name,
                     :user_data, :employee_data, :instructor_data, NOW())
                ON CONFLICT (erpnext_user_email)
                DO UPDATE SET
                    local_user_id = :user_id,
                    erpnext_employee_id = :employee_id,
                    erpnext_instructor_name = :instructor_name,
                    erpnext_user_data = :user_data,
                    erpnext_employee_data = :employee_data,
                    erpnext_instructor_data = :instructor_data,
                    last_synced_at = NOW()
            """),
            {
                "user_id": user_id,
                "email": email,
                "employee_id": employee_id,
                "instructor_name": instructor_name,
                "user_data": json.dumps(user_data),
                "employee_data": json.dumps(employee_data),
                "instructor_data": json.dumps(instructor_data)
            }
        )

    async def _upsert_teacher_classes(self, user_id: int, classes: List[Dict]):
        """Sync teacher class assignments"""

        # Clear old assignments
        self.db.execute(
            text("DELETE FROM erpnext_teacher_classes WHERE teacher_id = :teacher_id"),
            {"teacher_id": user_id}
        )

        # Insert new assignments - one row per subject per class
        for class_info in classes:
            student_group_name = class_info.get("name")
            program = class_info.get("program")
            batch = class_info.get("batch")
            academic_year = class_info.get("academic_year")
            academic_term = class_info.get("academic_term")

            # Parse grade and section from student_group_name (e.g., "2 A" -> grade=2, section=A)
            grade, section = self._parse_group_name(student_group_name)

            # Fetch subjects for this class from course schedules
            try:
                schedules = await self.client.get_course_schedule_by_student_group(student_group_name)
                subjects = []

                if schedules:
                    # Get unique subjects from schedules
                    for schedule in schedules:
                        course = schedule.get("course")
                        if course and course not in subjects:
                            subjects.append(course)

                # If we have subjects, create one row per subject
                if subjects:
                    for subject in subjects:
                        self.db.execute(
                            text("""
                                INSERT INTO erpnext_teacher_classes
                                    (teacher_id, student_group_name, program, batch, grade, section,
                                     subject, academic_year, academic_term, student_group_data)
                                VALUES
                                    (:teacher_id, :group_name, :program, :batch, :grade, :section,
                                     :subject, :academic_year, :academic_term, :group_data)
                            """),
                            {
                                "teacher_id": user_id,
                                "group_name": student_group_name,
                                "program": program,
                                "batch": batch,
                                "grade": grade,
                                "section": section,
                                "subject": subject,
                                "academic_year": academic_year,
                                "academic_term": academic_term,
                                "group_data": json.dumps(class_info)
                            }
                        )
                else:
                    # No subjects found, create one row without subject
                    self.db.execute(
                        text("""
                            INSERT INTO erpnext_teacher_classes
                                (teacher_id, student_group_name, program, batch, grade, section,
                                 subject, academic_year, academic_term, student_group_data)
                            VALUES
                                (:teacher_id, :group_name, :program, :batch, :grade, :section,
                                 :subject, :academic_year, :academic_term, :group_data)
                        """),
                        {
                            "teacher_id": user_id,
                            "group_name": student_group_name,
                            "program": program,
                            "batch": batch,
                            "grade": grade,
                            "section": section,
                            "subject": None,
                            "academic_year": academic_year,
                            "academic_term": academic_term,
                            "group_data": json.dumps(class_info)
                        }
                    )
            except Exception as e:
                logger.error(f"Error fetching subjects for {student_group_name}: {str(e)}")
                # Create row without subject on error
                self.db.execute(
                    text("""
                        INSERT INTO erpnext_teacher_classes
                            (teacher_id, student_group_name, program, batch, grade, section,
                             subject, academic_year, academic_term, student_group_data)
                        VALUES
                            (:teacher_id, :group_name, :program, :batch, :grade, :section,
                             :subject, :academic_year, :academic_term, :group_data)
                    """),
                    {
                        "teacher_id": user_id,
                        "group_name": student_group_name,
                        "program": program,
                        "batch": batch,
                        "grade": grade,
                        "section": section,
                        "subject": None,
                        "academic_year": academic_year,
                        "academic_term": academic_term,
                        "group_data": json.dumps(class_info)
                    }
                )

    def _upsert_student_mapping(
        self,
        user_id: int,
        student_id: str,
        student_data: Dict,
        grade: str,
        section: str
    ):
        """Save student mapping"""
        email = student_data.get("student_email_id") or student_data.get("user") or f"{student_id}@temp.school.com"

        self.db.execute(
            text("""
                INSERT INTO erpnext_student_mapping
                    (local_student_id, erpnext_student_id, erpnext_student_email,
                     erpnext_student_data, current_grade, current_section,
                     erpnext_student_name, roll_number, last_synced_at)
                VALUES
                    (:user_id, :student_id, :email, :student_data,
                     :grade, :section, :student_name, :roll_number, NOW())
                ON CONFLICT (erpnext_student_id)
                DO UPDATE SET
                    local_student_id = :user_id,
                    erpnext_student_email = :email,
                    erpnext_student_data = :student_data,
                    current_grade = :grade,
                    current_section = :section,
                    erpnext_student_name = :student_name,
                    roll_number = :roll_number,
                    last_synced_at = NOW()
            """),
            {
                "user_id": user_id,
                "student_id": student_id,
                "email": email,
                "student_data": json.dumps(student_data),
                "grade": grade,
                "section": section,
                "student_name": student_data.get("student_name"),
                "roll_number": student_data.get("group_roll_number")
            }
        )

    async def _upsert_student_groups(self, user_id: int, groups: List[Dict]):
        """
        Save student group (class/section) memberships

        Args:
            user_id: Local user ID
            groups: List of student groups from ERPNext
        """
        # Delete existing groups
        self.db.execute(
            text("DELETE FROM erpnext_student_groups WHERE student_id = :student_id"),
            {"student_id": user_id}
        )

        # Insert new groups
        for group in groups:
            group_name = group.get("group_name", "")
            grade, section = self._parse_group_name(group_name)

            self.db.execute(
                text("""
                    INSERT INTO erpnext_student_groups (
                        student_id, student_group_name, grade, section,
                        roll_number, academic_year, program, batch, is_active
                    )
                    VALUES (
                        :student_id, :group_name, :grade, :section,
                        :roll_number, :academic_year, :program, :batch, true
                    )
                """),
                {
                    "student_id": user_id,
                    "group_name": group_name,
                    "grade": grade,
                    "section": section,
                    "roll_number": group.get("roll_number"),
                    "academic_year": group.get("academic_year"),
                    "program": group.get("program"),
                    "batch": group.get("batch")
                }
            )

    def _parse_group_name(self, group_name: str) -> tuple:
        """
        Parse student group name to extract grade and section
        Examples: "2 A" -> ("2", "A"), "10 B" -> ("10", "B")
        """
        parts = group_name.strip().split()
        if len(parts) >= 2:
            return parts[0], parts[1]
        return group_name, ""

    def _extract_grades_from_classes(self, classes: List[Dict]) -> str:
        """Extract comma-separated grades from class list"""
        grades = set()
        for class_info in classes:
            group_name = class_info.get("name", "")
            grade, _ = self._parse_group_name(group_name)
            if grade:
                grades.add(grade)
        return ", ".join(sorted(grades))

    def _start_sync_log(self, sync_type: str, entity_id: str) -> int:
        """Start sync log and return log ID"""
        result = self.db.execute(
            text("""
                INSERT INTO erpnext_sync_logs
                    (sync_type, entity_id, status, operation, sync_started_at)
                VALUES
                    (:sync_type, :entity_id, 'in_progress', 'sync', NOW())
                RETURNING id
            """),
            {"sync_type": sync_type, "entity_id": entity_id}
        )
        self.db.commit()
        return result.fetchone()[0]

    def _complete_sync_log(self, log_id: int, status: str, records: int):
        """Mark sync as complete"""
        self.db.execute(
            text("""
                UPDATE erpnext_sync_logs
                SET status = :status,
                    records_processed = :records,
                    sync_completed_at = NOW(),
                    duration_seconds = EXTRACT(EPOCH FROM (NOW() - sync_started_at))
                WHERE id = :log_id
            """),
            {"log_id": log_id, "status": status, "records": records}
        )
        self.db.commit()

    def _fail_sync_log(self, log_id: int, error: str):
        """Mark sync as failed"""
        self.db.execute(
            text("""
                UPDATE erpnext_sync_logs
                SET status = 'failed',
                    error_message = :error,
                    sync_completed_at = NOW(),
                    duration_seconds = EXTRACT(EPOCH FROM (NOW() - sync_started_at))
                WHERE id = :log_id
            """),
            {"log_id": log_id, "error": error}
        )
        self.db.commit()


def get_sync_service(db: Session) -> ERPNextSyncService:
    """Get sync service instance"""
    return ERPNextSyncService(db=db)
