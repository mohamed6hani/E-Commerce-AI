from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
async def register_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(models.user.User).filter(models.user.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.user.User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}


@router.post("/login")
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = (
        db.query(models.user.User)
        .filter(models.user.User.email == email, models.user.User.password == password)
        .first()
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "id": user.id}