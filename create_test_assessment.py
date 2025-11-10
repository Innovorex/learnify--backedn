import requests
import json
from datetime import datetime, timedelta

# Login as teacher
login_response = requests.post(
    "http://localhost:3003/auth/login",
    json={"email": "mary@gmail.com", "password": "mary@123"}
)
token = login_response.json()["access_token"]

# Calculate start and end times
now = datetime.now()
start_time = now.strftime("%Y-%m-%dT%H:%M:%S")
end_time = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")

# Create V2 assessment with multiple question types
print("📝 Creating V2 Assessment with Multiple Question Types...")
response = requests.post(
    "http://localhost:3003/teacher/k12/create-assessment-v2",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    },
    json={
        "teacher_id": 2,
        "class_name": "10",
        "section": "A",
        "subject": "Mathematics",
        "chapter": "Real Numbers",
        "start_time": start_time,
        "end_time": end_time,
        "duration_minutes": 30,
        "question_spec": {
            "multiple_choice": 3,
            "multi_select": 1,
            "true_false": 2,
            "short_answer": 1,
            "fill_blank": 1,
            "ordering": 0
        }
    }
)

print(json.dumps(response.json(), indent=2))
