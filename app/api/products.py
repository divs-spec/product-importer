from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Product
from ..schemas import ProductOut, ProductCreate

router = APIRouter(prefix="/products")

@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).limit(50).all()

@router.post("", response_model=ProductOut)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/bulk")
def bulk_delete_products(
    confirm: bool = Query(False),
    db: Session = Depends(get_db)
):
    if not confirm:
        return {"error": "Confirmation required"}
    db.query(Product).delete()
    db.commit()
    return {"status": "all products deleted"}
