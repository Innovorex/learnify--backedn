# routers/modules.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Module
from schemas import ModuleOut

router = APIRouter(prefix="/modules", tags=["modules"])

from schemas import ModuleIn

@router.post("/", response_model=ModuleOut, status_code=201)
def create_module(module_in: ModuleIn, db: Session = Depends(get_db)):
    db_module = Module(**module_in.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/", response_model=list[ModuleOut])
def list_modules(db: Session = Depends(get_db)):
    return db.query(Module).all()
