from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reemplaza estos valores por los de tu entorno local
DB_USER = "root"
DB_PASSWORD = "contraseña"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "agropedidos"

# URL de conexión
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el engine
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear la sesión
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
