from database import SessionLocal
from models import User
from security import hash_password

db = SessionLocal()

# Create user
email = "mani@gmail.com"
password = "mani@123"

existing_user = db.query(User).filter_by(email=email).first()
if existing_user:
    print(f"User {email} already exists")
else:
    user = User(
        name="Mani",
        email=email,
        password_hash=hash_password(password),
        role="teacher"
    )
    db.add(user)
    db.commit()
    print(f"User created: {email} with password: {password}")

db.close()
