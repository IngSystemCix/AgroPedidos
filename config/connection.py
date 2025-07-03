from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configura tus credenciales de HeidiSQL
DB_USER = "root"
DB_PASSWORD = "123456"
DB_HOST = "127.0.0.1"
DB_PORT = "3307"
DB_NAME = "agropedidos_db"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
