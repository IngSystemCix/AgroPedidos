from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from config.connection import Base

class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    payment_type = Column(String(50), nullable=False)  # Card o Yape
    status = Column(String(20), default="Pending")     # Success, Error, Pending
    payment_date = Column(DateTime, default=datetime.now)
