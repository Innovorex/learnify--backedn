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
        """Fetch employee details linked to user"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/Employee",
                    headers=self.headers_data,
                    params={"filters": f'[["user_id","=","{user_id}"]]'}
                )

                if response.status_code == 200:
                    data = response.json().get("data", [])
                    return data[0] if data else None
                return None

            except Exception as e:
                logger.error(f"Error fetching employee for user {user_id}: {str(e)}")
                return None

    async def get_instructor_by_email(self, email: str) -> Optional[Dict]:
        """Fetch instructor details by email"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # First try to get instructor by email
                response = await client.get(
                    f"{self.api_base}/Instructor",
                    headers=self.headers_data,
                    params={"filters": f'[["email","=","{email}"]]'}
                )

                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if data:
                        instructor_name = data[0].get("name")
                        # Fetch full instructor details
                        detail_response = await client.get(
                            f"{self.api_base}/Instructor/{instructor_name}",
                            headers=self.headers_data
                        )
                        if detail_response.status_code == 200:
                            return detail_response.json().get("data", {})
                return None

            except Exception as e:
                logger.error(f"Error fetching instructor {email}: {str(e)}")
                return None

    async def get_teacher_classes(self, instructor_name: str) -> List[Dict]:
        """
        Fetch classes assigned to an instructor
        Returns list of student groups where instructor is assigned
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.api_base}/Student Group",
                    headers=self.headers_data,
                    params={"filters": f'[["instructors","like","%{instructor_name}%"]]'}
                )

                if response.status_code == 200:
                    return response.json().get("data", [])
                return []

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
                response = await client.get(
                    f"{self.api_base}/Course Schedule",
                    headers=self.headers_data,
                    params={"filters": f'[["student_group","=","{student_group}"]]'}
                )

                if response.status_code == 200:
                    return response.json().get("data", [])
                return []

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

    async def sync_teacher_complete(self, email: str) -> Dict[str, Any]:
        """
        Complete teacher sync - fetch all related data

        Returns:
            {
                "user": {...},
                "employee": {...},
                "instructor": {...},
                "classes": [...],
                "subjects": [...]
            }
        """
        result = {
            "success": False,
            "user": None,
            "employee": None,
            "instructor": None,
            "classes": [],
            "subjects": set()
        }

        # Fetch user
        user = await self.get_user_by_email(email)
        if not user:
            result["error"] = "User not found in ERPNext"
            return result

        result["user"] = user

        # Fetch employee
        employee = await self.get_employee_by_user_id(email)
        result["employee"] = employee

        # Fetch instructor
        instructor = await self.get_instructor_by_email(email)
        result["instructor"] = instructor

        if instructor:
            instructor_name = instructor.get("name")

            # Fetch classes
            classes = await self.get_teacher_classes(instructor_name)
            result["classes"] = classes

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