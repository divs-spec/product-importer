# app/workers/importer.py
import csv
from celery import Celery
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from ..database import SessionLocal
from ..models import Product, ImportJob
from ..config import REDIS_URL

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

BATCH_SIZE = 1000

@celery.task(bind=True)
def import_products(self, job_id: str, file_path: str):
    db = SessionLocal()
    job = db.get(ImportJob, job_id)

    try:
        job.status = "parsing"
        db.commit()

        processed = 0
        batch = []

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                batch.append({
                    "sku": row["sku"],
                    "name": row.get("name"),
                    "description": row.get("description"),
                })

                if len(batch) >= BATCH_SIZE:
                    upsert_products(db, batch)
                    processed += len(batch)
                    batch.clear()

                    job.processed = processed
                    job.status = "importing"
                    db.commit()

            if batch:
                upsert_products(db, batch)
                processed += len(batch)

        job.processed = processed
        job.status = "completed"
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()
    finally:
        db.close()


def upsert_products(db, rows):
    stmt = insert(Product).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=[func.lower(Product.sku)],
        set_={
            "name": stmt.excluded.name,
            "description": stmt.excluded.description,
        },
    )
    db.execute(stmt)
    db.commit()
