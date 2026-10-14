from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np
import sys
from pathlib import Path

from .. import models, database

# Add the root of the project to sys.path so we can import shared modules
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.embedding_pipeline import EmbeddingPipeline  # type: ignore
from shared.recommender import RecommenderEngine  # type: ignore
from shared.dynamic_pricing import DynamicPricing, PricingInputs  # type: ignore

router = APIRouter(prefix="/ai", tags=["ai"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/recommend")
async def recommend_products(query: str, db: Session = Depends(get_db), top_k: int = 5):
    products = db.query(models.product.Product).all()
    if not products:
        return []
    # Convert products to dict format
    product_dicts = [p.__dict__ for p in products]
    pipeline = EmbeddingPipeline()
    vectors = [pipeline.embed_product(p) for p in product_dicts]
    vectors_np = np.stack(vectors)
    qvec = pipeline.embed_text(query)
    rec = RecommenderEngine(vectors_np)
    indices = rec.recommend(qvec, top_k=top_k)
    return [products[i] for i in indices]


@router.get("/price")
async def dynamic_price(product_id: int, demand_factor: float = 0.5, competitor_price: float = 0.0, db: Session = Depends(get_db)):
    product = db.get(models.product.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    dp = DynamicPricing()
    inputs = PricingInputs(
        base_price=product.price,
        demand_factor=demand_factor,
        stock_level=product.stock,
        competitor_price=competitor_price,
    )
    price = dp.adjust_price(inputs)
    return {"product_id": product_id, "dynamic_price": price}