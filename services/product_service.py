from config.connection import SessionLocal
from models.product import Product

def get_all_products():
    db = SessionLocal()
    try:
        return db.query(Product).all()
    finally:
        db.close()
