from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum
from config.connection import Base
import enum

class PaymentMethodEnum(enum.Enum):
    D = "D"
    Y = "Y"

class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Usuario.id"))
    created_at = Column(DateTime)
    total = Column(Numeric(10, 2))
    payment_method = Column(Enum(PaymentMethodEnum))
