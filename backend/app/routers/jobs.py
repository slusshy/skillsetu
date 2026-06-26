import json
import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from app.database import SessionLocal, WorkerProfile, SavedJob, JobAlert

router = APIRouter()

JOBS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "jobs.json")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "in")

def load_jobs() -> List[Dict[str, Any]]:
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

class JobMatchRequest(BaseModel):
    skills: List[str]

class JobMatch(BaseModel):
    title: str
    company: str
    location: str
    salary_min: float | None = None
    salary_max: float | None = None
    description: str
    redirect_url: str
    match_percentage: float
    missing_skills: List[str]

def normalize_skills(raw: Any) -> List[str]:
    if isinstance(raw, list):
        return [str(s).strip() for s in raw if str(s).strip()]
    if isinstance(raw, str):
        # tolerate comma-separated as well
        return [s.strip() for s in raw.split(",") if s.strip()]
    return []


def calculate_match(profile_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
    profile_skills = normalize_skills(profile_skills)
    job_skills = normalize_skills(job_skills)
    if not job_skills:
        return {"match_percentage": 0.0, "missing_skills": []}

    profile_set = set((s or "").lower().strip() for s in profile_skills)
    job_set = set((s or "").lower().strip() for s in job_skills)
    job_set = {s for s in job_set if s}

    matched = profile_set.intersection(job_set)
    missing = sorted(list(job_set - profile_set))

    base = (len(matched) / len(job_set)) * 100 if job_set else 0.0
    soft_bonus = 0.0
    soft_terms = ["team", "safety", "time management", "communication", "supervision", "cleanliness", "organization", "english", "hindi"]
    for term in soft_terms:
        if any(term in s for s in profile_set) and any(term in s for s in job_set):
            soft_bonus += 5
    match_pct = min(100.0, base + soft_bonus)

    return {
        "match_percentage": round(match_pct, 1),
        "missing_skills": missing,
    }

@router.post("/match-jobs", response_model=List[JobMatch])
def match_jobs(request: JobMatchRequest):
    adzuna_jobs = []
    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        try:
            adzuna_jobs = fetch_adzuna_jobs(request.skills)
        except Exception as e:
            print(f"Adzuna fetch failed: {e}")
    if not adzuna_jobs:
        adzuna_jobs = load_jobs()
    results = []
    for job in adzuna_jobs:
        job_skills = job.get("skills", [])
        match = calculate_match(request.skills, job_skills)
        results.append(JobMatch(
            title=job.get("title", ""),
            company=job.get("company", ""),
            location=job.get("location", ""),
            salary_min=job.get("salary_min"),
            salary_max=job.get("salary_max"),
            description=job.get("description", ""),
            redirect_url=job.get("redirect_url", ""),
            match_percentage=match["match_percentage"],
            missing_skills=match["missing_skills"]
        ))
    results.sort(key=lambda x: x.match_percentage, reverse=True)
    return results[:10]

@router.get("/profile/{profile_id}/matches", response_model=List[JobMatch])
def get_profile_matches(profile_id: int, db: Session = Depends(lambda: SessionLocal())):
    profile = db.query(WorkerProfile).filter(WorkerProfile.id == profile_id).first()
    if not profile:
        return []
    skills = normalize_skills(profile.skills)
    return match_jobs(JobMatchRequest(skills=skills))


@router.get("/search")
def search_jobs(q: str, location: str = "", page: int = 1):
    results = []
    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        try:
            results = fetch_adzuna_jobs_query(q, location=location, page=page)
        except Exception as e:
            print(f"Adzuna fetch failed: {e}")
    if not results:
        results = load_jobs()
    return results[:20]

@router.post("/save/{adzuna_id}")
def save_job(adzuna_id: str, db: Session = Depends(lambda: SessionLocal())):
    existing = db.query(SavedJob).filter(SavedJob.adzuna_id == adzuna_id).first()
    if existing:
        return {"saved": True, "id": existing.id}
    saved = SavedJob(adzuna_id=adzuna_id)
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return {"saved": True, "id": saved.id}

@router.delete("/save/{adzuna_id}")
def unsave_job(adzuna_id: str, db: Session = Depends(lambda: SessionLocal())):
    job = db.query(SavedJob).filter(SavedJob.adzuna_id == adzuna_id).first()
    if not job:
        return {"saved": False}
    db.delete(job)
    db.commit()
    return {"saved": False}

@router.get("/saved")
def get_saved_jobs(db: Session = Depends(lambda: SessionLocal())):
    saved = db.query(SavedJob).all()
    adzuna_ids = [s.adzuna_id for s in saved]
    jobs = []
    if ADZUNA_APP_ID and ADZUNA_APP_KEY and adzuna_ids:
        try:
            jobs = fetch_adzuna_by_ids(adzuna_ids)
        except Exception as e:
            print(f"Adzuna fetch by id failed: {e}")
    if not jobs:
        jobs = [{"adzuna_id": aid, "title": f"Saved Job {i+1}", "company": "", "location": "", "description": "", "redirect_url": "", "salary_min": None, "salary_max": None} for i, aid in enumerate(adzuna_ids)]
    return jobs

@router.post("/alerts")
def create_alert(keywords: str, db: Session = Depends(lambda: SessionLocal())):
    alert = JobAlert(keywords=keywords)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"id": alert.id, "keywords": alert.keywords}

@router.get("/alerts")
def list_alerts(db: Session = Depends(lambda: SessionLocal())):
    return db.query(JobAlert).all()

def fetch_adzuna_jobs(skills: List[str]) -> List[Dict[str, Any]]:
    if ADZUNA_APP_ID and ADZUNA_APP_KEY and skills:
        try:
            query = " ".join(skills[:5])
            url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/1"
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": query,
                "results_per_page": 10,
                "content-type": "application/json",
            }
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if results:
                jobs: List[Dict[str, Any]] = []
                for r in results:
                    title = r.get("title") or ""
                    desc = r.get("description") or ""
                    loc = r.get("location", {}).get("display_name") if isinstance(r.get("location"), dict) else ""
                    co  = r.get("company", {}).get("display_name") if isinstance(r.get("company"), dict) else ""
                    min_sal = r.get("salary_min")
                    max_sal = r.get("salary_max")
                    redirect = r.get("redirect_url") or ""
                    jobs.append({
                        "title": title,
                        "company": co,
                        "location": loc,
                        "salary_min": min_sal,
                        "salary_max": max_sal,
                        "description": desc,
                        "redirect_url": redirect,
                        "skills": skills,
                    })
                return jobs
            # Retry simpler query if no results on combined terms
            simple_query = skills[0] if skills else ""
            if simple_query and simple_query != query:
                params["what"] = simple_query
                resp = requests.get(url, params=params, timeout=20)
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results", [])
                if results:
                    jobs = []
                    for r in results:
                        title = r.get("title") or ""
                        desc = r.get("description") or ""
                        loc = r.get("location", {}).get("display_name") if isinstance(r.get("location"), dict) else ""
                        co  = r.get("company", {}).get("display_name") if isinstance(r.get("company"), dict) else ""
                        min_sal = r.get("salary_min")
                        max_sal = r.get("salary_max")
                        redirect = r.get("redirect_url") or ""
                        jobs.append({
                            "title": title,
                            "company": co,
                            "location": loc,
                            "salary_min": min_sal,
                            "salary_max": max_sal,
                            "description": desc,
                            "redirect_url": redirect,
                            "skills": skills,
                        })
                    return jobs
        except Exception as e:
            print(f"Adzuna fetch failed: {e}")
    return []


def fetch_adzuna_jobs_query(q: str, location: str = "", page: int = 1) -> List[Dict[str, Any]]:
    query = q.strip()
    loc = location.strip()
    if not query:
        return []
    url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "where": loc,
        "results_per_page": 20,
        "content-type": "application/json",
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    jobs: List[Dict[str, Any]] = []
    for r in results:
        title = r.get("title") or ""
        desc = r.get("description") or ""
        loc = r.get("location", {}).get("display_name") if isinstance(r.get("location"), dict) else ""
        co = r.get("company", {}).get("display_name") if isinstance(r.get("company"), dict) else ""
        min_sal = r.get("salary_min")
        max_sal = r.get("salary_max")
        redirect = r.get("redirect_url") or ""
        adzuna_id = str(r.get("id") or r.get("adzuna_id") or "")
        jobs.append({
            "adzuna_id": adzuna_id,
            "title": title,
            "company": co,
            "location": loc,
            "salary_min": min_sal,
            "salary_max": max_sal,
            "description": desc,
            "redirect_url": redirect,
            "skills": [x.strip() for x in q.split(" ") if x.strip()],
        })
    return jobs


def fetch_adzuna_by_ids(adzuna_ids: List[str]) -> List[Dict[str, Any]]:
    # Best-effort: search with id terms to approximate saved jobs when Adzuna supports lookup by id
    jobs: List[Dict[str, Any]] = []
    for aid in adzuna_ids[:20]:
        try:
            url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/1"
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": aid,
                "results_per_page": 1,
                "content-type": "application/json",
            }
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if results:
                r = results[0]
                jobs.append({
                    "adzuna_id": aid,
                    "title": r.get("title") or "",
                    "company": r.get("company", {}).get("display_name") if isinstance(r.get("company"), dict) else "",
                    "location": r.get("location", {}).get("display_name") if isinstance(r.get("location"), dict) else "",
                    "salary_min": r.get("salary_min"),
                    "salary_max": r.get("salary_max"),
                    "description": r.get("description") or "",
                    "redirect_url": r.get("redirect_url") or "",
                    "skills": [aid],
                })
        except Exception as e:
            print(f"Adzuna by-id fetch failed for {aid}: {e}")
    return jobs
