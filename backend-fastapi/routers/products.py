from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/products", tags=["products"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def list_products(db: Session = Depends(get_db)):
    return db.query(models.product.Product).all()


@router.post("/")
async def create_product(product: models.product.Product, db: Session = Depends(get_db)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.product.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product