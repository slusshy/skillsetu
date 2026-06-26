
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, Float
from typing import Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./skillsetu.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SavedJob(Base):
    __tablename__ = "saved_jobs"
    id = Column(Integer, primary_key=True, index=True)
    adzuna_id = Column(String, unique=True, index=True)

class JobAlert(Base):
    __tablename__ = "job_alerts"
    id = Column(Integer, primary_key=True, index=True)
    keywords = Column(String)

class WorkerProfile(Base):
    __tablename__ = "worker_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)
    work_experience = Column(Text, nullable=False)
    skills = Column(Text, nullable=True)
    experience_summary = Column(Text, nullable=True)
    recommended_job_category = Column(String(255), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "location": self.location,
            "work_experience": self.work_experience,
            "skills": self.skills,
            "experience_summary": self.experience_summary,
            "recommended_job_category": self.recommended_job_category,
        }