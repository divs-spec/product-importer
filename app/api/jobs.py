# app/api/jobs.py
import time, json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..database import SessionLocal
from ..models import ImportJob

router = APIRouter()

@router.get("/jobs/{job_id}/events")
def job_events(job_id: str):
    def event_stream():
        db = SessionLocal()
        last = None
        while True:
            job = db.get(ImportJob, job_id)
            payload = {
                "status": job.status,
                "processed": job.processed,
                "total": job.total,
                "error": job.error,
            }
            if payload != last:
                yield f"data: {json.dumps(payload)}\n\n"
                last = payload
            if job.status in ("completed", "failed"):
                break
            time.sleep(1)
        db.close()

    return StreamingResponse(event_stream(), media_type="text/event-stream")
