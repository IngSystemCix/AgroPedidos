from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import mysql.connector

# Configuración de la base de datos
DB_USER = "root"
DB_PASSWORD = "123456"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "agropedidos_db"

# SQLAlchemy
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Conexión directa con mysql-connector
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
