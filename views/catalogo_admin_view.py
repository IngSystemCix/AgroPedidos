from PIL import Image
import customtkinter as ctk
import os
from services.product_service import get_all_products

class CatalogoAdminView(ctk.CTkFrame):
    def __init__(self, master, usuario, navigate):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.navigate = navigate
        self.configure(fg_color="#f3fdf2")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # HEADER
        header = ctk.CTkFrame(self, fg_color="#ffffff", height=80)
        header.pack(fill="x", side="top")

        try:
            logo_img = Image.open("./resources/images/logo.png")
            logo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
            ctk.CTkLabel(header, image=logo, text="").pack(side="left", padx=10, pady=10)
        except:
            pass

        ctk.CTkLabel(header, text="AGROPEDIDOS", font=("Segoe UI", 28, "bold"), text_color="#1a8341").pack(side="left", padx=10)

        user_section = ctk.CTkFrame(header, fg_color="transparent")
        user_section.pack(side="right", padx=20)
        ctk.CTkLabel(user_section, text="👨‍💼", font=("Segoe UI", 18)).pack(side="left")
        ctk.CTkLabel(user_section, text="Administrador", font=("Segoe UI", 14)).pack(side="left", padx=5)
        ctk.CTkLabel(user_section, text=self.usuario.username, font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(user_section, text="Cerrar sesión", width=100, fg_color="#ff4d4d", hover_color="#cc0000", command=self.navigate_logout).pack(side="left", padx=10)

        # NAVIGATION
        nav_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        nav_frame.pack(pady=(5, 0))

        secciones = [("Catálogo", "catalogo"), ("Gestión de Productos", "gestion"), ("Inventario", "inventario"), ("Ventas", "ventas")]
        for label, destino in secciones:
            ctk.CTkButton(nav_frame, text=label, width=150, command=lambda d=destino: self.navigate(d)).pack(side="left", padx=10)

        # CANVAS
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#f3fdf2", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.products_frame = ctk.CTkFrame(self.canvas, fg_color="#f3fdf2")
        self.products_window = self.canvas.create_window((0, 0), window=self.products_frame, anchor="nw")

        self.products_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.products_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-int(event.delta / 120), "units"))

        self.load_products()

    def load_products(self, columns=5):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        products = get_all_products()

        for i in range(columns):
            self.products_frame.grid_columnconfigure(i, weight=1)

        for index, product in enumerate(products):
            row = index // columns
            col = index % columns
            self.create_product_card(product, row, col)

    def create_product_card(self, product, row, col):
        card_width = 230
        card_height = 280

        card = ctk.CTkFrame(self.products_frame, corner_radius=12, fg_color="#ffffff", width=card_width, height=card_height)
        card.grid(row=row, column=col, padx=15, pady=15)
        card.grid_propagate(False)

        image = self.get_product_image(product)
        if image:
            ctk.CTkLabel(card, image=image, text="").pack(pady=(10, 5))
        else:
            ctk.CTkLabel(card, text="Sin imagen").pack(pady=(10, 5))

        ctk.CTkLabel(card, text=product.name, font=("Segoe UI", 14, "bold"), text_color="#1a8341").pack(pady=2)
        ctk.CTkLabel(card, text=f"S/ {product.price:.2f}", font=("Segoe UI", 14)).pack(pady=2)
        ctk.CTkLabel(card, text=f"Stock: {product.stock}", font=("Arial", 12)).pack(pady=2)

    def get_product_image(self, product):
        try:
            path = os.path.join("resources", "images", product.image_url or "noimage.png")
            if os.path.exists(path):
                img = Image.open(path)
                return ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
        except:
            pass
        return None

    def navigate_logout(self):
        self.navigate("logout")
