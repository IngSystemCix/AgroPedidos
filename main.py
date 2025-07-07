import tkinter as tk
import customtkinter as ctk
from views.catalogo_admin_view import CatalogoAdminView
from views.gestion_productos_view import GestionProductosView
from views.inventario_view import InventarioView
from views.ventas_view import VentasView
from views.detalle_pedido_view import DetallePedidoView
from views.product_catalog import ProductCatalogView
from models.usuario import Usuario

class MainApp(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.title("Panel de AgroPedidos")
        self.geometry("1280x720")
        self.current_view = None
        self.usuario = usuario

        self.create_menu()
        self.show_view("catalogo")  # Vista inicial

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        if self.usuario.rol == "Administrador":
            admin_menu = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label="Administrador", menu=admin_menu)
            admin_menu.add_command(label="Catálogo", command=lambda: self.show_view("catalogo"))
            admin_menu.add_command(label="Gestión de Productos", command=lambda: self.show_view("gestion"))
            admin_menu.add_command(label="Inventario", command=lambda: self.show_view("inventario"))
            admin_menu.add_command(label="Ventas", command=lambda: self.show_view("ventas"))
            admin_menu.add_command(label="Pedidos", command=lambda: self.show_view("pedidos"))
            admin_menu.add_separator()
            admin_menu.add_command(label="Cerrar sesión", command=self.cerrar_sesion)
        else:
            cliente_menu = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label="Cliente", menu=cliente_menu)
            cliente_menu.add_command(label="Catálogo", command=lambda: self.show_view("catalogo"))
            cliente_menu.add_separator()
            cliente_menu.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

    def show_view(self, view_name):
        if self.current_view:
            self.current_view.destroy()

        common_args = {
            "usuario": self.usuario,
            "navigate": self.show_view
        }

        if self.usuario.rol == "Administrador":
            if view_name == "catalogo":
                self.current_view = CatalogoAdminView(self, **common_args)
            elif view_name == "gestion":
                self.current_view = GestionProductosView(self, **common_args)
            elif view_name == "inventario":
                self.current_view = InventarioView(self, **common_args)
            elif view_name == "ventas":
                self.current_view = VentasView(self, **common_args)
            elif view_name == "pedidos":
                self.current_view = DetallePedidoView(self, **common_args)
            else:
                self.current_view = tk.Label(self, text="Vista no encontrada", font=("Arial", 18))
        else:
            self.current_view = ProductCatalogView(self, usuario=self.usuario)

        self.current_view.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        self.destroy()  # Cierra ventana principal actual

        import customtkinter as ctk
        from views.login import LoginView

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        login_root = ctk.CTk()
        login_root.title("AgroPedidos")
        login_root.configure(fg_color="white")
        login_root.iconbitmap("./resources/images/favicon.ico")

        window_width = 800
        window_height = 700
        screen_width = login_root.winfo_screenwidth()
        screen_height = login_root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        login_root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        login_view = LoginView(master=login_root)
        login_view.pack(fill="both", expand=True)
        login_root.mainloop()

# Solo para pruebas directas del main.py
if __name__ == "__main__":
    from models.usuario import Usuario
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = MainApp(Usuario(id=1, username="admin", rol="Administrador"))
    app.mainloop()
