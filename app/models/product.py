# app/models/product.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models import Base


class Product(Base):
    __tablename__ = "products"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    category_id  = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    name         = Column(String(150), nullable=False)
    description  = Column(Text, nullable=True)
    price        = Column(DECIMAL(10, 2), nullable=False)
    image_url    = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at   = Column(DateTime, default=func.now(), nullable=False)
    updated_at   = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    category    = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product id={self.id} name={self.name} price={self.price}>"