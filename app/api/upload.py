import shutil, uuid
from fastapi import APIRouter, UploadFile
from ..database import SessionLocal
from ..models import ImportJob
from ..celery_worker import import_products

router = APIRouter()

@router.post("/upload")
def upload_csv(file: UploadFile):
    path = f"/tmp/{uuid.uuid4()}.csv"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    db = SessionLocal()
    job = ImportJob()
    db.add(job)
    db.commit()

    import_products.delay(job.id, path)
    return {"job_id": job.id}

