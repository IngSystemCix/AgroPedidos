from sqlalchemy import Column, Integer, DateTime, Float, String
from datetime import datetime
from config.connection import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
