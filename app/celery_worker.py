import csv
from celery import Celery
from sqlalchemy.dialects.postgresql import insert
from .database import SessionLocal
from .models import Product, ImportJob
from .config import REDIS_URL

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)

@celery.task(bind=True)
def import_products(self, job_id, file_path):
    db = SessionLocal()
    job = db.query(ImportJob).get(job_id)
    try:
        with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            job.total = len(rows)
            job.status = "importing"
            db.commit()

            batch = []
            for i, row in enumerate(rows, 1):
                stmt = insert(Product).values(
                    sku=row["sku"],
                    name=row.get("name"),
                    description=row.get("description"),
                ).on_conflict_do_update(
                    index_elements=[func.lower(Product.sku)],
                    set_={
                        "name": row.get("name"),
                        "description": row.get("description"),
                    }
                )
                db.execute(stmt)

                if i % 1000 == 0:
                    db.commit()
                    job.processed = i
                    db.commit()

            db.commit()
            job.status = "completed"
            job.processed = job.total
            db.commit()

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()
    finally:
        db.close()

