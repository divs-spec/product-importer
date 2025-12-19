from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Product
from ..schemas import ProductOut, ProductCreate

router = APIRouter(prefix="/products")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# ----------------------------
# BULK DELETE (ADD THIS BELOW)
# ----------------------------
@router.delete("/bulk")
def bulk_delete(
    confirm: bool = Query(False),
    db: Session = Depends(get_db)
):
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Confirmation required to delete all products"
        )

    db.query(Product).delete()
    db.commit()

    return {
        "status": "success",
        "message": "All products deleted"
    }
