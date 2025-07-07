from config.connection import get_connection

# Clase Product local para representar cada fila
class Product:
    def __init__(self, row):
        self.id, self.name, self.price, self.unit, self.stock, self.image_url = row

# Obtener todos los productos
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, unit, stock, image_url FROM Product")
    rows = cursor.fetchall()
    conn.close()
    return [Product(row) for row in rows]

# Agregar un nuevo producto
def add_product(name, price, unit, stock, image_url, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO Product (name, price, unit, stock, image_url, usuario_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name, price, unit, stock, image_url, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()

# Actualizar un producto existente
def update_product(product_id, name, price, unit, stock):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE Product
        SET name = %s, price = %s, unit = %s, stock = %s
        WHERE id = %s
    """
    cursor.execute(sql, (name, price, unit, stock, product_id))
    conn.commit()
    cursor.close()
    conn.close()

# Eliminar un producto por ID
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Product WHERE id = %s"
    cursor.execute(sql, (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
