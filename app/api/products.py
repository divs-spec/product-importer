from fastapi import APIRouter
from ..database import SessionLocal
from ..models import Product

router = APIRouter(prefix="/products")

@router.get("")
def list_products():
    db = SessionLocal()
    return db.query(Product).limit(50).all()

@router.delete("/bulk")
def bulk_delete():
    db = SessionLocal()
    db.query(Product).delete()
    db.commit()
    return {"status": "deleted"}

