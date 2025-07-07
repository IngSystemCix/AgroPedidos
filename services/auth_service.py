from sqlalchemy.orm import Session
from config.connection import SessionLocal
from models.usuario import Usuario
from utils.security import hash_password, verify_password

# Obtener usuario por nombre
def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

# Crear nuevo usuario (por defecto con rol Cliente)
def create_usuario(username: str, password: str, rol: str = "Cliente"):
    db = SessionLocal()
    try:
        existing = get_usuario_by_username(db, username)
        if existing:
            return None  # Ya existe
        nuevo_usuario = Usuario(
            username=username,
            password=hash_password(password),
            rol=rol
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    finally:
        db.close()

# Login
def authenticate(username: str, password: str):
    db = SessionLocal()
    try:
        user = get_usuario_by_username(db, username)
        if user and verify_password(password, user.password):
            return user
        return None
    finally:
        db.close()
