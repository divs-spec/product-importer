from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ImportJob

router = APIRouter(prefix="/upload", tags=["Upload"])


class CSVImportRequest(BaseModel):
    file_url: str


@router.post("")
def upload_csv(
    payload: CSVImportRequest,
    db: Session = Depends(get_db)
):
    # 1. Create import job
    job = ImportJob(
        status="queued",
        total=0,
        processed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # 2. DO NOT call Celery from Vercel
    # Worker will poll for queued jobs

    return {
        "job_id": job.id,
        "file_url": payload.file_url,
        "status": "queued"
    }
