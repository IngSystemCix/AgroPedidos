from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from config.connection import Base

class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Usuario.id"))  # cambio aquí
    stock = Column(Integer)
    name = Column(String(60))
    price = Column(Numeric(10, 2))
    unit = Column(String(20))  # agregado para unidad ("por kg", etc.)
    image_url = Column(String(100))
