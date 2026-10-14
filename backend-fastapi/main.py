from fastapi import FastAPI

from .database import Base, engine
from .routers import products, users, orders, ai


# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="eCommerce AI FastAPI Backend")

# Include routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {"message": "eCommerce AI FastAPI backend running"}