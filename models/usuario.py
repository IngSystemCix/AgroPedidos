from sqlalchemy import Column, Integer, String, Enum
from config.connection import Base
import enum

class RolEnum(enum.Enum):
    Cliente = "Cliente"
    Administrador = "Administrador"

class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
