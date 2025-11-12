"""
ERPNext API Client for Learnify-Teach Integration
Handles authentication and data fetching from Innovorex ERPNext DevPortal
"""

import os
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ERPNextClient:
    """Client for interacting with Innovorex ERPNext API"""

    def __init__(self):
        self.base_url = "https://devportal.innovorex.co.in"
        self.api_base = f"{self.base_url}/api/erpnext"
        self.auth_endpoint = f"{self.base_url}/api/public/login"

        # API credentials for data fetching
        self.api_key = os.getenv("ERPNEXT_API_KEY", "51b4af3bca0e0feea200ca1a280cca19c584be6e")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET", "0d6b32667965a7a3c602b592fbd52ff85281bf1b")
        self.token = f"{self.api_key}:{self.api_secret}"

        self.headers_data = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json"
        }

        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user against ERPNext portal

        Args:
            email: User email address
            password: User password

        Returns:
            Dict containing authentication result with user data and token

        Raises:
            HTTPException: If authentication fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.auth_endpoint,
                    json={
                        "email": email,
                        "password": password
                    },
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code != 200:
                    logger.error(f"ERPNext auth failed: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": "Invalid credentials",
                        "status_code": response.status_code
                    }

                data = response.json()

                # Response format: {"success": true, "message": "...", "data": {...}}
                if data.get("success"):
                    logger.info(f"ERPNext authentication successful for {email}")
                    return {
                        "success": True,
                        "user": data.get("data", {}).get("user"),
                        "email": data.get("data", {}).get("email"),
                        "role": data.get("data", {}).get("role"),
                        "token": data.get("data", {}).get("token"),
                        "name": data.get("data", {}).get("name")
                    }
                else:
                    return {
                        "success": False,
                        "error": data.get("message", "Authentication failed")
                    }

            except httpx.TimeoutException:
                logger.error(f"ERPNext authentication timeout for {email}")
                return {"success": False, "error": "Authentication timeout"}
            except Exception as e:
                logger.error(f"ERPNext authentication error: {str(e)}")
                return {"success": False, "error": f"Authentication error: {str(e)}"}

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Fetch user details from ERPNext by email"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/User/{email}",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    return response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching user {email}: {str(e)}")
                return None

    async def get_employee_by_user_id(self, user_id: str) -> Optional[Dict]:
        """Fetch employee details linked to user - iterates through all employees"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Get all employee IDs
                response = await client.get(
                    f"{self.api_base}/Employee",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    employee_list = response.json().get("data", [])

                    # Fetch each employee and check user_id
                    for emp_item in employee_list:
                        emp_id = emp_item.get("name")
                        emp_response = await client.get(
                            f"{self.api_base}/Employee/{emp_id}",
                            headers=self.headers_data
                        )

                        if emp_response.status_code == 200:
                            employee = emp_response.json().get("data", {})
                            if employee.get("user_id") == user_id:
                                return employee

                return None

            except Exception as e:
                logger.error(f"Error fetching employee for user {user_id}: {str(e)}")
                return None

    async def get_instructor_by_employee_id(self, employee_id: str) -> Optional[Dict]:
        """Fetch instructor details by employee ID"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Get all instructors
                response = await client.get(
                    f"{self.api_base}/Instructor",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    instructor_list = response.json().get("data", [])

                    # Fetch each instructor and check employee field
                    for inst_item in instructor_list:
                        inst_name = inst_item.get("name")
                        inst_response = await client.get(
                            f"{self.api_base}/Instructor/{inst_name}",
                            headers=self.headers_data
                        )

                        if inst_response.status_code == 200:
                            instructor = inst_response.json().get("data", {})
                            if instructor.get("employee") == employee_id:
                                return instructor

                return None

            except Exception as e:
                logger.error(f"Error fetching instructor for employee {employee_id}: {str(e)}")
                return None

    async def get_teacher_classes(self, instructor_name: str) -> List[Dict]:
        """
        Fetch classes assigned to an instructor
        Returns list of student groups where instructor is assigned

        Note: Filtering on child tables doesn't work via REST API,
        so we fetch all Student Groups and check each one's instructors
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # First, get list of all Student Groups
                response = await client.get(
                    f"{self.api_base}/Student Group",
                    headers=self.headers_data,
                    params={"limit_page_length": 999}
                )

                if response.status_code != 200:
                    logger.error(f"Failed to fetch Student Groups: {response.status_code}")
                    return []

                groups_list = response.json().get("data", [])
                matching_groups = []

                # Iterate through each group and fetch full details
                for group_item in groups_list:
                    group_name = group_item.get("name")

                    # Fetch full Student Group details (includes instructors child table)
                    group_response = await client.get(
                        f"{self.api_base}/Student Group/{group_name}",
                        headers=self.headers_data
                    )

                    if group_response.status_code == 200:
                        group_details = group_response.json().get("data", {})

                        # Check if instructor is in the instructors child table
                        instructors = group_details.get("instructors", [])
                        for instructor_entry in instructors:
                            if instructor_entry.get("instructor") == instructor_name:
                                matching_groups.append(group_details)
                                break

                return matching_groups

            except Exception as e:
                logger.error(f"Error fetching classes for {instructor_name}: {str(e)}")
                return []

    async def get_student_group_details(self, group_name: str) -> Optional[Dict]:
        """Fetch detailed student group information including students"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/Student Group/{group_name}",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    return response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching student group {group_name}: {str(e)}")
                return None

    async def get_course_schedule_by_student_group(self, student_group: str) -> List[Dict]:
        """Fetch course schedules for a student group to get subjects taught"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # First get list of matching schedules
                response = await client.get(
                    f"{self.api_base}/Course Schedule",
                    headers=self.headers_data,
                    params={"filters": f'[["student_group","=","{student_group}"]]'}
                )

                if response.status_code != 200:
                    logger.error(f"Failed to fetch Course Schedules: {response.status_code}")
                    return []

                schedule_list = response.json().get("data", [])
                detailed_schedules = []

                # Fetch full details for each schedule
                for schedule_item in schedule_list:
                    schedule_name = schedule_item.get("name")
                    detail_response = await client.get(
                        f"{self.api_base}/Course Schedule/{schedule_name}",
                        headers=self.headers_data
                    )

                    if detail_response.status_code == 200:
                        detailed_schedules.append(detail_response.json().get("data", {}))

                return detailed_schedules

            except Exception as e:
                logger.error(f"Error fetching course schedule for {student_group}: {str(e)}")
                return []

    async def get_student_details(self, student_id: str) -> Optional[Dict]:
        """Fetch student details by student ID"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/Student/{student_id}",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    return response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching student {student_id}: {str(e)}")
                return None

    async def get_students_by_group(self, group_name: str) -> List[Dict]:
        """Fetch all students in a student group"""
        group_details = await self.get_student_group_details(group_name)

        if not group_details:
            return []

        students = group_details.get("students", [])
        student_details = []

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for student_entry in students:
                student_id = student_entry.get("student")
                if student_id:
                    try:
                        response = await client.get(
                            f"{self.api_base}/Student/{student_id}",
                            headers=self.headers_data
                        )
                        if response.status_code == 200:
                            student_details.append(response.json().get("data", {}))
                    except Exception as e:
                        logger.error(f"Error fetching student {student_id}: {str(e)}")

        return student_details

    async def get_student_by_email(self, email: str) -> Optional[Dict]:
        """
        Get student details by email address

        Args:
            email: Student email address

        Returns:
            Dict with student data or None if not found
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Search for student by email
                response = await client.get(
                    f"{self.api_base}/Student",
                    headers=self.headers_data,
                    params={
                        "filters": f'[["student_email_id","=","{email}"]]',
                        "fields": '["name","student_name","first_name","last_name","student_email_id","gender","date_of_birth","student_mobile_number"]'
                    }
                )

                if response.status_code != 200:
                    logger.error(f"Failed to search student by email: {response.status_code}")
                    return None

                data = response.json().get("data", [])
                if not data:
                    logger.warning(f"Student not found with email: {email}")
                    return None

                student_id = data[0].get("name")

                # Fetch full student details
                detail_response = await client.get(
                    f"{self.api_base}/Student/{student_id}",
                    headers=self.headers_data
                )

                if detail_response.status_code == 200:
                    return detail_response.json().get("data", {})

                return None

            except Exception as e:
                logger.error(f"Error fetching student by email {email}: {str(e)}")
                return None

    async def get_student_groups_for_student(self, student_id: str) -> List[Dict]:
        """
        Get all student groups (classes/sections) a student belongs to

        Args:
            student_id: ERPNext Student ID (e.g., EDU-STU-2024-00001)

        Returns:
            List of student groups with enrollment details
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Fetch all Student Groups
                response = await client.get(
                    f"{self.api_base}/Student Group",
                    headers=self.headers_data,
                    params={"limit_page_length": 999}
                )

                if response.status_code != 200:
                    logger.error(f"Failed to fetch Student Groups: {response.status_code}")
                    return []

                groups_list = response.json().get("data", [])
                student_groups = []

                # Iterate through each group and check if student is enrolled
                for group_item in groups_list:
                    group_name = group_item.get("name")

                    # Fetch full Student Group details (includes students child table)
                    group_response = await client.get(
                        f"{self.api_base}/Student Group/{group_name}",
                        headers=self.headers_data
                    )

                    if group_response.status_code == 200:
                        group_details = group_response.json().get("data", {})

                        # Check if student is in the students child table
                        students = group_details.get("students", [])
                        for student_entry in students:
                            if student_entry.get("student") == student_id and student_entry.get("active"):
                                student_groups.append({
                                    "group_name": group_details.get("name"),
                                    "program": group_details.get("program"),
                                    "batch": group_details.get("batch"),
                                    "academic_year": group_details.get("academic_year"),
                                    "roll_number": student_entry.get("group_roll_number")
                                })
                                break

                return student_groups

            except Exception as e:
                logger.error(f"Error fetching student groups for {student_id}: {str(e)}")
                return []

    async def get_program_enrollment(self, student_id: str) -> Optional[Dict]:
        """
        Get student's program enrollment details

        Args:
            student_id: ERPNext Student ID

        Returns:
            Dict with enrollment details or None
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/Program Enrollment",
                    headers=self.headers_data,
                    params={
                        "filters": f'[["student","=","{student_id}"],["docstatus","=",1]]',
                        "fields": '["name","program","academic_year","enrollment_date"]'
                    }
                )

                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if data:
                        return data[0]

                return None

            except Exception as e:
                logger.error(f"Error fetching program enrollment for {student_id}: {str(e)}")
                return None

    async def get_program(self, program_name: str) -> Optional[Dict]:
        """Fetch Program details (includes department for board info)"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                from urllib.parse import quote
                response = await client.get(
                    f"{self.api_base}/Program/{quote(program_name)}",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    return response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching program {program_name}: {str(e)}")
                return None

    async def get_department(self, department_name: str) -> Optional[Dict]:
        """Fetch Department details (contains board name)"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                from urllib.parse import quote
                response = await client.get(
                    f"{self.api_base}/Department/{quote(department_name)}",
                    headers=self.headers_data
                )

                if response.status_code == 200:
                    return response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching department {department_name}: {str(e)}")
                return None

    async def get_board_for_program(self, program_name: str) -> str:
        """
        Get board name from program
        Flow: Program → Department → department_name (Board)
        """
        program = await self.get_program(program_name)
        if not program:
            return "Not specified"

        department_name = program.get("department")
        if not department_name:
            return "Not specified"

        department = await self.get_department(department_name)
        if not department:
            return "Not specified"

        # Extract board name (e.g., "State - SRS" → "State")
        board = department.get("department_name", "Not specified")
        return board

    async def sync_teacher_complete(self, email: str) -> Dict[str, Any]:
        """
        Complete teacher sync - fetch all related data

        Returns:
            {
                "success": bool,
                "user": {...},
                "employee": {...},
                "instructor": {...},
                "classes": [...],
                "subjects": [...],
                "board": "..."
            }
        """
        result = {
            "success": False,
            "user": None,
            "employee": None,
            "instructor": None,
            "classes": [],
            "subjects": set(),
            "board": "Not specified"
        }

        # Fetch user
        user = await self.get_user_by_email(email)
        if not user:
            result["error"] = "User not found in ERPNext"
            return result

        result["user"] = user

        # Fetch employee
        employee = await self.get_employee_by_user_id(email)
        if not employee:
            result["error"] = "Employee not found in ERPNext"
            return result

        result["employee"] = employee

        # Fetch instructor using employee ID
        employee_id = employee.get("name")
        instructor = await self.get_instructor_by_employee_id(employee_id)
        if not instructor:
            result["error"] = "Instructor profile not found"
            return result

        result["instructor"] = instructor

        instructor_name = instructor.get("name")

        # Fetch classes (Student Groups)
        classes = await self.get_teacher_classes(instructor_name)
        result["classes"] = classes

        # Get board from first class's program
        if classes:
            first_class = classes[0]
            program_name = first_class.get("program")
            if program_name:
                board = await self.get_board_for_program(program_name)
                result["board"] = board

        # Fetch subjects from course schedules
        for class_group in classes:
            group_name = class_group.get("name")
            schedules = await self.get_course_schedule_by_student_group(group_name)
            for schedule in schedules:
                course = schedule.get("course")
                if course:
                    result["subjects"].add(course)

        result["subjects"] = list(result["subjects"])
        result["success"] = True

        return result

    async def test_connection(self) -> Dict[str, Any]:
        """Test ERPNext API connection"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/User",
                    headers=self.headers_data,
                    params={"limit_page_length": 1}
                )

                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "message": "Connection successful" if response.status_code == 200 else "Connection failed"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }


# Singleton instance
_erpnext_client = None

def get_erpnext_client() -> ERPNextClient:
    """Get or create ERPNext client singleton"""
    global _erpnext_client
    if _erpnext_client is None:
        _erpnext_client = ERPNextClient()
    return _erpnext_client