from config.connection import get_connection

class Product:
    def __init__(self, row):
        self.id, self.name, self.price, self.unit, self.stock, self.image_url = row

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, unit, stock, image_url FROM Product WHERE is_active = TRUE")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Product(row) for row in rows]

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

def update_product(product_id, name, price, unit, stock, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE Product
        SET name = %s, price = %s, unit = %s, stock = %s, image_url = %s
        WHERE id = %s
    """
    cursor.execute(sql, (name, price, unit, stock, image_url, product_id))
    conn.commit()
    cursor.close()
    conn.close()

def soft_delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Product SET is_active = FALSE WHERE id = %s"
    cursor.execute(sql, (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

def product_exists(name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM Product WHERE LOWER(name) = LOWER(%s)"
    cursor.execute(sql, (name,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result > 0
