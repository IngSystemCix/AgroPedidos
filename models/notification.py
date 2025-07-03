from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text
from config.connection import Base
import enum

class NotificationStatusEnum(enum.Enum):
    S = "S"
    E = "E"
    P = "P"

class Notification(Base):
    __tablename__ = "Notification"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.id"))
    message = Column(Text)
    status = Column(Enum(NotificationStatusEnum))
    sent_at = Column(DateTime)
