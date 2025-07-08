from config.connection import get_connection

def get_all_orders_with_user():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.id, o.created_at, o.total, o.payment_method, u.username AS cliente
            FROM `order` o
            JOIN usuario u ON o.usuario_id = u.id
            ORDER BY o.created_at DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"[❌] Error al obtener pedidos: {e}")
        return []

def get_order_by_id(order_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.id, o.created_at, o.total, o.payment_method, u.username AS cliente
            FROM `order` o
            JOIN usuario u ON o.usuario_id = u.id
            WHERE o.id = %s
        """
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"[❌] Error al obtener pedido por ID: {e}")
        return None

def get_order_items_by_order_id(order_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.name AS nombre, oi.quantity AS cantidad, p.unit, p.price
            FROM orderitem oi
            JOIN product p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"[❌] Error al obtener items del pedido: {e}")
        return []
