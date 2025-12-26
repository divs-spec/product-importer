import uuid
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ImportJob

router = APIRouter(prefix="/upload")


@router.post("")
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    job = ImportJob(status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)

    # IMPORTANT:
    # Do NOT process CSV here.
    # Vercel is API-only.
    # Worker on Railway will pick this job.

    return {
        "job_id": job.id,
        "status": "queued"
    }
