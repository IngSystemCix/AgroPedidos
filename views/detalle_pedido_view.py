import customtkinter as ctk
from tkinter import ttk
from services.order_service import get_order_by_id, get_order_items_by_order_id

class DetallePedidoView(ctk.CTkToplevel):
    def __init__(self, master, order_id):
        super().__init__(master)
        self.order_id = order_id
        self.title(f"Detalle del Pedido #{order_id}")
        self.geometry("750x520")
        self.configure(fg_color="#f3fdf2")
        self.grab_set()  # Modal

        self.order = get_order_by_id(order_id)
        self.order_items = get_order_items_by_order_id(order_id)

        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(self, text=f"Detalle del Pedido #{self.order_id}", font=("Arial", 22, "bold")).pack(pady=10)

        info_frame = ctk.CTkFrame(self, fg_color="white")
        info_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(info_frame, text=f"👤 Cliente: {self.order['cliente']}", font=("Arial", 14)).pack(anchor="w", pady=2)
        ctk.CTkLabel(info_frame, text=f"💳 Método de Pago: {self.order['payment_method']}", font=("Arial", 14)).pack(anchor="w", pady=2)
        ctk.CTkLabel(info_frame, text=f"📅 Fecha: {self.order['created_at']}", font=("Arial", 14)).pack(anchor="w", pady=2)
        ctk.CTkLabel(info_frame, text=f"💰 Total Pagado: S/. {self.order['total']:.2f}", font=("Arial", 14, "bold")).pack(anchor="w", pady=2)

        # Tabla de productos
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("Producto", "Cantidad", "Precio Unitario", "Subtotal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

        for item in self.order_items:
            cantidad_str = f"{item['cantidad']} {item['unit']}"
            precio_unitario = item['price']
            subtotal = item['cantidad'] * precio_unitario
            self.tree.insert("", "end", values=(
                item["nombre"],
                cantidad_str,
                f"S/. {precio_unitario:.2f}",
                f"S/. {subtotal:.2f}"
            ))

        ctk.CTkButton(self, text="Cerrar", command=self.destroy).pack(pady=10)
