from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from config.connection import Base

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(1), default="P")  # S: Success, E: Error, P: Pending
    created_at = Column(DateTime, default=datetime.now)
