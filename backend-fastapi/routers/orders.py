from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/orders", tags=["orders"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def list_orders(db: Session = Depends(get_db)):
    return db.query(models.order.Order).all()


@router.post("/")
async def create_order(user_id: int, total: float, status: str = "pending", db: Session = Depends(get_db)):
    order = models.order.Order(user_id=user_id, total=total, status=status)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order