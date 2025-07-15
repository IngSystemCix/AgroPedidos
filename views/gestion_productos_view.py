from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image
from services.product_service import get_all_products, soft_delete_product
from views.agregar_producto_view import AgregarProductoView
from views.editar_producto_view import EditarProductoView

class GestionProductosView(ctk.CTkFrame):
    def __init__(self, master, usuario, navigate):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.navigate = navigate
        self.configure(fg_color="#f3fdf2")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
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
        ctk.CTkButton(
            user_section,
            text="Cerrar sesión",
            width=100,
            fg_color="#ff4d4d",
            hover_color="#cc0000",
            command=self.navigate_logout
        ).pack(side="left", padx=10)

        nav_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        nav_frame.pack(pady=(5, 0))
        secciones = [("Catálogo", "catalogo"), ("Gestión de Productos", "gestion"), ("Inventario", "inventario"), ("Ventas", "ventas")]
        for label, destino in secciones:
            ctk.CTkButton(nav_frame, text=label, width=150, command=lambda d=destino: self.navigate(d)).pack(side="left", padx=10)

        agregar_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        agregar_frame.pack(pady=10, fill="x")

        ctk.CTkButton(
            agregar_frame,
            text="+ Agregar Producto",
            height=40,
            width=200,
            fg_color="#1a8341",
            hover_color="#157d35",
            font=("Segoe UI", 14, "bold"),
            command=self.abrir_ventana_agregar
        ).pack(side="right", padx=20)

        tabla_frame = ctk.CTkFrame(self, fg_color="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Nombre", "Precio", "Stock", "Unidad", "Editar", "Eliminar"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            if col in ("Nombre",):
                self.tree.column(col, anchor="w", width=180)
            elif col in ("Editar", "Eliminar"):
                self.tree.column(col, anchor="center", width=80)
            else:
                self.tree.column(col, anchor="center", width=100)

        self.tree.pack(fill="both", expand=True, pady=10, padx=10)
        self.tree.bind("<ButtonRelease-1>", self.manejar_click_accion)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = get_all_products()
        for p in productos:
            self.tree.insert("", "end", values=(
                p.id,
                p.name,
                f"S/ {p.price:.2f}",
                p.stock,
                p.unit,
                "✏️",
                "🗑️"
            ))

    def manejar_click_accion(self, event):
        item_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if not item_id or col not in ("#6", "#7"):
            return

        producto_values = self.tree.item(item_id)["values"]
        product_id = producto_values[0]

        producto = next((p for p in get_all_products() if p.id == product_id), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if col == "#6":
            self.abrir_modal_editar(producto)
        elif col == "#7":
            self.eliminar_producto(producto)

    def abrir_modal_editar(self, producto):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Editar Producto")
        ventana.geometry("500x600")
        EditarProductoView(ventana, producto=producto, on_success=self.recargar_productos)

    def eliminar_producto(self, producto):
        confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de eliminar '{producto.name}'?")
        if confirm:
            try:
                soft_delete_product(producto.id)  # Cambio aquí
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                self.recargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

    def abrir_ventana_agregar(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Producto")
        ventana.geometry("500x600")
        AgregarProductoView(ventana, usuario_id=self.usuario.id, on_success=self.recargar_productos)

    def recargar_productos(self):
        self.cargar_datos()

    def navigate_logout(self):
        self.navigate("logout")
