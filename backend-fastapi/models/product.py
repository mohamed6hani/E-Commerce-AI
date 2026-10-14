from sqlalchemy import Column, Integer, String, Float
from ..database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    category = Column(String, default="")
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String, default="")