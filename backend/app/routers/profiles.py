from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import SessionLocal, WorkerProfile
from app.services import extract_profile

router = APIRouter()

class ProfileCreate(BaseModel):
    name: str
    age: Optional[int] = None
    location: Optional[str] = None
    work_experience: str
    language: Optional[str] = "en"

class ProfileResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]
    location: Optional[str]
    work_experience: str
    skills: Optional[List[str]]
    experience_summary: Optional[str]
    recommended_job_category: Optional[str]

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/profile", response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    extracted = extract_profile(profile.work_experience, language=profile.language or "en")
    db_profile = WorkerProfile(
        name=profile.name,
        age=profile.age,
        location=profile.location,
        work_experience=profile.work_experience,
        skills=", ".join(extracted["skills"]),
        experience_summary=extracted["experience_summary"],
        recommended_job_category=extracted["recommended_job_category"],
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return ProfileResponse(
        id=db_profile.id,
        name=db_profile.name,
        age=db_profile.age,
        location=db_profile.location,
        work_experience=db_profile.work_experience,
        skills=extracted["skills"],
        experience_summary=extracted["experience_summary"],
        recommended_job_category=extracted["recommended_job_category"],
    )

@router.get("/profiles", response_model=List[ProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    profiles = db.query(WorkerProfile).all()
    return [
        ProfileResponse(
            id=p.id,
            name=p.name,
            age=p.age,
            location=p.location,
            work_experience=p.work_experience,
            skills=p.skills.split(", ") if p.skills else [],
            experience_summary=p.experience_summary,
            recommended_job_category=p.recommended_job_category,
        )
        for p in profiles
    ]