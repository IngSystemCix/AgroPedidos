# views/components/product_card.py
import customtkinter as ctk
from PIL import Image
import os

class ProductCard:
    def __init__(self, parent, product, row, col, add_to_cart_callback):
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color="#ffffff", width=150, height=300)
        card.grid(row=row, column=col, padx=15, pady=15)
        card.grid_propagate(False)

        product._qty_var = ctk.StringVar(value="1")

        image_path = os.path.join("resources", "images", product.image_url)
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            ctk.CTkLabel(card, image=img_ctk, text="").pack(pady=(10, 5))
        else:
            ctk.CTkLabel(card, text="Sin imagen", font=("Arial", 12, "italic")).pack()

        ctk.CTkLabel(card, text=product.name, font=("Segoe UI", 16, "bold"), text_color="#1a8341").pack()
        ctk.CTkLabel(card, text=f"S/ {product.price:.2f}", font=("Segoe UI", 18, "bold"), text_color="#1a8341").pack()

        unidad = getattr(product, "unit", "por unidad")
        ctk.CTkLabel(card, text=unidad, font=("Segoe UI", 12, "bold"),
                     text_color="#b05c1e", fg_color="#fef3c7").pack(pady=(0, 5))

        qty_frame = ctk.CTkFrame(card, fg_color="transparent")
        qty_frame.pack(pady=5)

        def decrease_qty():
            val = int(product._qty_var.get())
            if val > 1:
                product._qty_var.set(str(val - 1))

        def increase_qty():
            val = int(product._qty_var.get())
            product._qty_var.set(str(val + 1))

        ctk.CTkButton(qty_frame, text="-", width=30, command=decrease_qty).pack(side="left", padx=5)
        ctk.CTkLabel(qty_frame, textvariable=product._qty_var, width=30).pack(side="left")
        ctk.CTkButton(qty_frame, text="+", width=30, command=increase_qty).pack(side="left", padx=5)

        ctk.CTkButton(card, text="🛒 Agregar al carrito", font=("Segoe UI", 14, "bold"),
                      fg_color="#1a8341", hover_color="#146c34",
                      command=lambda: add_to_cart_callback(product, int(product._qty_var.get()))
        ).pack(pady=(10, 0), padx=10, fill="x")
