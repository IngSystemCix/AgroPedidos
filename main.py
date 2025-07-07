import tkinter as tk
import customtkinter as ctk
from views.login import LoginView
from views.catalogo_admin_view import CatalogoAdminView
from views.gestion_productos_view import GestionProductosView
from views.inventario_view import InventarioView
from views.ventas_view import VentasView
from views.detalle_pedido_view import DetallePedidoView
from views.product_catalog import ProductCatalogView

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AgroPedidos")
        self.geometry("1280x720")
        self.current_view = None
        self.usuario = None

        self.show_login()

    def show_login(self):
        self.clear_view()
        login_view = LoginView(master=self, on_login_success=self.start_main_app)
        login_view.pack(fill="both", expand=True)

    def start_main_app(self, usuario):
        self.usuario = usuario
        self.clear_view()
        self.create_menu()
        self.show_view("catalogo")

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
        self.clear_view()

        common_args = {
            "usuario": self.usuario,
            "navigate": self.show_view
        }

        if view_name == "logout":
            self.cerrar_sesion()
            return

        if self.usuario.rol == "Administrador":
            views = {
                "catalogo": CatalogoAdminView,
                "gestion": GestionProductosView,
                "inventario": InventarioView,
                "ventas": VentasView,
                "pedidos": DetallePedidoView
            }
            self.current_view = views.get(view_name, lambda *a, **kw: tk.Label(self, text="Vista no encontrada", font=("Arial", 18)))(self, **common_args)
        else:
            self.current_view = ProductCatalogView(self, usuario=self.usuario, navigate=self.show_view)

        self.current_view.pack(fill="both", expand=True)

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def cerrar_sesion(self):
        self.usuario = None
        self.clear_view()
        self.show_login()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = MainApp()
    app.mainloop()
