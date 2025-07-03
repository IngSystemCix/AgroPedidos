from sqlalchemy import Column, Integer, ForeignKey, Numeric
from config.connection import Base

class OrderItem(Base):
    __tablename__ = "OrderItem"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.id"))
    product_id = Column(Integer, ForeignKey("Product.id"))
    quantity = Column(Integer)
    subtotal = Column(Numeric(10, 2))
