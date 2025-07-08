import customtkinter as ctk
from services.product_service import get_all_products
from views.header_user import HeaderUser
from views.search_bar import SearchBar
from views.product_card import ProductCard
from views.cart_modal import CartModal

class ProductCatalogView(ctk.CTkFrame):
    def __init__(self, master, usuario, navigate):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.navigate = navigate

        self.configure(fg_color="#f3fdf2")
        self.pack(fill="both", expand=True)

        self.carrito = []
        self.carrito_total = 0.0
        self.cart_button = None
        self.search_term = ""

        self.create_widgets()

    def create_widgets(self):
        HeaderUser(self, self.usuario, self.navigate)
        self.search_bar = SearchBar(self, self.perform_search)

        self.canvas_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        self.canvas_frame.pack(fill="both", expand=True, pady=10)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#f3fdf2", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.products_frame = ctk.CTkFrame(self.canvas, fg_color="#f3fdf2")
        self.products_window = self.canvas.create_window((0, 0), window=self.products_frame, anchor="nw")

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.products_window, width=e.width))
        self.products_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Scroll solo cuando el mouse entra al canvas
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.load_products()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), "units")

    def perform_search(self):
        self.search_term = self.search_bar.search_entry.get().lower()
        self.load_products()

    def load_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        all_products = get_all_products()
        if self.search_term:
            all_products = [p for p in all_products if self.search_term in p.name.lower()]

        columns = 5  # Fijo: 5 productos por fila

        # Centrado de columnas
        for col in range(columns):
            self.products_frame.grid_columnconfigure(col, weight=1)

        for index, product in enumerate(all_products):
            row = index // columns
            col = index % columns
            ProductCard(self.products_frame, product, row, col, self.agregar_al_carrito)

    def agregar_al_carrito(self, producto, cantidad):
        for i, (p, c) in enumerate(self.carrito):
            if p.id == producto.id:
                self.carrito[i] = (p, c + cantidad)
                break
        else:
            self.carrito.append((producto, cantidad))

        self.carrito_total = sum(float(p.price) * c for p, c in self.carrito)
        self.mostrar_boton_carrito()

    def mostrar_boton_carrito(self):
        texto = f"🛒 Ver carrito - S/ {self.carrito_total:.2f}"

        if self.cart_button:
            self.cart_button.configure(text=texto)
            return

        self.cart_button = ctk.CTkButton(
            self,
            text=texto,
            font=("Segoe UI", 16, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            corner_radius=20,
            command=self.abrir_carrito,
        )
        self.cart_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    def abrir_carrito(self):
        if not self.carrito:
            return
        CartModal(self, self.carrito, self.carrito_total, self.reset_carrito, self.usuario)

    def reset_carrito(self):
        self.carrito.clear()
        self.carrito_total = 0.0
        if self.cart_button:
            self.cart_button.destroy()
            self.cart_button = None
