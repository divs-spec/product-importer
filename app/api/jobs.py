from fastapi import APIRouter
from ..database import SessionLocal
from ..models import ImportJob

router = APIRouter()

@router.get("/jobs/{job_id}")
def job_status(job_id: str):
    db = SessionLocal()
    job = db.query(ImportJob).get(job_id)
    return job.__dict__

