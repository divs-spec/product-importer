from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ImportJob

router = APIRouter(prefix="/upload")


class CSVImportRequest(BaseModel):
    file_url: str


@router.post("")
def upload_csv(
    payload: CSVImportRequest,
    db: Session = Depends(get_db)
):
    job = ImportJob(status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)

    # Send job to Celery (Railway)
    import_products.delay(job.id, payload.file_url)

    return {
        "job_id": job.id,
        "status": "queued"
    }
