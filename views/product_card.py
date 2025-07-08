import customtkinter as ctk
from PIL import Image
import os

class ProductCard:
    def __init__(self, parent, product, row, col, add_to_cart_callback):
        self.product = product
        self.card = ctk.CTkFrame(parent, corner_radius=12, fg_color="#ffffff", width=150, height=300)
        self.card.grid(row=row, column=col, padx=15, pady=15)
        self.card.grid_propagate(False)

        self.product._qty_var = ctk.StringVar(value="1")

        image_path = os.path.join("resources", "images", product.image_url)
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            ctk.CTkLabel(self.card, image=img_ctk, text="").pack(pady=(10, 5))
        else:
            ctk.CTkLabel(self.card, text="Sin imagen", font=("Arial", 12, "italic")).pack()

        # Nombre del producto
        ctk.CTkLabel(self.card, text=product.name, font=("Segoe UI", 16, "bold"), text_color="#1a8341").pack()

        # Stock disponible (con referencia para actualizarlo)
        self.stock_label = ctk.CTkLabel(self.card, text=f"Stock: {product.stock}", font=("Segoe UI", 12),
                                        text_color="#6b7280")
        self.stock_label.pack(pady=(0, 0))

        # Precio
        ctk.CTkLabel(self.card, text=f"S/ {product.price:.2f}", font=("Segoe UI", 18, "bold"),
                     text_color="#1a8341").pack()

        # Unidad de medida
        unidad = getattr(product, "unit", "por unidad")
        ctk.CTkLabel(self.card, text=unidad, font=("Segoe UI", 12, "bold"),
                     text_color="#b05c1e", fg_color="#fef3c7").pack(pady=(0, 5))

        # Controles de cantidad
        qty_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        qty_frame.pack(pady=5)

        def decrease_qty():
            val = int(self.product._qty_var.get())
            if val > 1:
                self.product._qty_var.set(str(val - 1))

        def increase_qty():
            val = int(self.product._qty_var.get())
            if val < self.product.stock:
                self.product._qty_var.set(str(val + 1))

        ctk.CTkButton(qty_frame, text="-", width=30, command=decrease_qty).pack(side="left", padx=5)
        ctk.CTkLabel(qty_frame, textvariable=self.product._qty_var, width=30).pack(side="left")
        ctk.CTkButton(qty_frame, text="+", width=30, command=increase_qty).pack(side="left", padx=5)

        # Botón agregar al carrito
        ctk.CTkButton(self.card, text="🛒 Agregar al carrito", font=("Segoe UI", 14, "bold"),
                      fg_color="#1a8341", hover_color="#146c34",
                      command=lambda: add_to_cart_callback(product, int(self.product._qty_var.get()))
        ).pack(pady=(10, 0), padx=10, fill="x")

    def reset_quantity(self):
        """Restablece la cantidad a 1 al cerrar el modal del carrito."""
        if hasattr(self.product, "_qty_var"):
            self.product._qty_var.set("1")

    def update_stock_display(self, new_stock):
        """Actualiza el stock visual y limita cantidad si excede el nuevo stock."""
        self.product.stock = new_stock
        self.stock_label.configure(text=f"Stock: {new_stock}")
        current_qty = int(self.product._qty_var.get())
        if current_qty > new_stock:
            self.product._qty_var.set(str(new_stock if new_stock > 0 else 1))
