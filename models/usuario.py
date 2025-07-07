from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # ← Rol como string: 'Cliente' o 'Administrador'

    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}', rol='{self.rol}')>"
