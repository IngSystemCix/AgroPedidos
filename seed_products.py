from config.connection import SessionLocal
from models.product import Product
from models.usuario import Usuario  # <--- AÑADE ESTA LÍNEA


db = SessionLocal()

productos = [
    {"name": "Tomate", "price": 2.50, "stock": 100, "unit": "por kg", "image_url": "tomate.jpg"},
    {"name": "Papa", "price": 1.90, "stock": 150, "unit": "por kg", "image_url": "papa.jpg"},
    {"name": "Zanahoria", "price": 1.50, "stock": 120, "unit": "por kg", "image_url": "zanahoria.jpg"},
    {"name": "Lechuga", "price": 1.80, "stock": 80, "unit": "por unidad", "image_url": "lechuga.jpg"},
    {"name": "Cebolla", "price": 2.20, "stock": 110, "unit": "por kg", "image_url": "cebolla.jpg"},
    {"name": "Manzana", "price": 3.50, "stock": 70, "unit": "por kg", "image_url": "manzana.jpg"},
    {"name": "Plátano", "price": 2.10, "stock": 90, "unit": "por kg", "image_url": "platano.jpg"},
    {"name": "Mandarina", "price": 2.80, "stock": 60, "unit": "por kg", "image_url": "mandarina.jpg"},
    {"name": "Aguacate", "price": 4.20, "stock": 50, "unit": "por unidad", "image_url": "aguacate.jpg"},
    {"name": "Maíz", "price": 1.75, "stock": 100, "unit": "por kg", "image_url": "maiz.jpg"},
    {"name": "Zapallo", "price": 2.90, "stock": 65, "unit": "por unidad", "image_url": "zapallo.jpg"},
    {"name": "Apio", "price": 1.60, "stock": 85, "unit": "por unidad", "image_url": "apio.jpg"},
    {"name": "Culantro", "price": 0.80, "stock": 200, "unit": "por atado", "image_url": "culantro.jpg"},
]

# Asignamos todos al usuario_id 2 (asumiendo que es un Cliente)
for prod in productos:
    producto = Product(
        usuario_id=4,  # Cambiar si el cliente tiene otro ID
        name=prod["name"],
        price=prod["price"],
        stock=prod["stock"],
        unit=prod["unit"],
        image_url=f"resources/images/{prod['image_url']}"
    )
    db.add(producto)

db.commit()
db.close()

print("✅ Productos insertados correctamente.")
