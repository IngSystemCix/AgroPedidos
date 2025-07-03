from sqlalchemy.orm import Session
from config.connection import SessionLocal
from models.usuario import Usuario
from utils.security import hash_password, verify_password

# Obtener usuario por nombre
def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

# Crear usuario (admin o cliente)
def create_usuario(username: str, password: str, rol: str = "Cliente"):
    db = SessionLocal()
    try:
        existing = get_usuario_by_username(db, username)
        if existing:
            raise Exception("El usuario ya existe")

        usuario = Usuario(
            username=username,
            password=hash_password(password),
            rol=rol
        )
        db.add(usuario)
        db.commit()
        return usuario
    finally:
        db.close()

# Autenticación en login
def authenticate(username: str, password: str):
    db = SessionLocal()
    try:
        user = get_usuario_by_username(db, username)
        if user and verify_password(password, user.password):
            return user  # Retorna el objeto Usuario completo
        return None
    finally:
        db.close()
