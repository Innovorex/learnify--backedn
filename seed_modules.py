# seed_modules.py
from database import SessionLocal, engine, Base
from models import Module

Base.metadata.create_all(bind=engine)
db = SessionLocal()

default_modules = [
    ("Subject Knowledge & Content Expertise",
     "Tests subject mastery, cross-disciplinary links, application",
     "mcq"),
    ("Pedagogical Skills & Classroom Practice",
     "Lesson planning, classroom management, student engagement",
     "mcq"),
    ("Use of Technology & Innovation",
     "ICT, digital tools, blended learning, innovative methods",
     "mcq"),
    ("Professional Growth & Collaboration",
     "Workshops, training, peer mentoring, CPD logs",
     "submission"),
    ("Student Learning Outcomes",
     "Academic & non-academic outcomes, improvement tracking",
     "outcome"),
    ("Assessment & Feedback",
     "Formative/summative, constructive feedback, fair evaluation",
     "mcq"),
    ("Inclusivity, Values & Dispositions",
     "Sensitivity to diversity, empathy, respect, holistic growth",
     "mcq"),
    ("Community & Parent Engagement",
     "Parent-school partnership, community involvement",
     "submission"),
    ("Professional Ethics & Teacher Accountability",
     "Integrity, reflection, responsibility, teacher conduct",
     "mcq"),
    ("Student Well-being & Holistic Development",
     "Counseling, socio-emotional development, life skills",
     "submission"),
]

for name, desc, atype in default_modules:
    if not db.query(Module).filter_by(name=name).first():
        db.add(Module(name=name, description=desc, assessment_type=atype))

db.commit()
db.close()
print("10 Modules seeded successfully")
