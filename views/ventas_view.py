from PIL import Image
import customtkinter as ctk
from tkinter import ttk, messagebox
import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from services.order_service import get_all_orders_with_user
from views.detalle_pedido_view import DetallePedidoView

class VentasView(ctk.CTkFrame):
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

        secciones = [
            ("Catálogo", "catalogo"),
            ("Gestión de Productos", "gestion"),
            ("Inventario", "inventario"),
            ("Ventas", "ventas")
        ]
        for label, destino in secciones:
            ctk.CTkButton(nav_frame, text=label, width=150, command=lambda d=destino: self.navigate(d)).pack(side="left", padx=10)

        # CONTENIDO VENTAS
        contenido = ctk.CTkFrame(self, fg_color="#f3fdf2")
        contenido.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(contenido, text="Lista de Ventas", font=("Arial", 20, "bold")).pack(pady=10)

        export_frame = ctk.CTkFrame(contenido, fg_color="transparent")
        export_frame.pack(anchor="e", pady=5)

        self.btn_export_excel = ctk.CTkButton(export_frame, text="Exportar Excel", command=self.exportar_excel)
        self.btn_export_excel.pack(side="left", padx=5)

        self.btn_export_xml = ctk.CTkButton(export_frame, text="Exportar XML", command=self.exportar_xml)
        self.btn_export_xml.pack(side="left")

        # Tabla de ventas
        columns = ("ID", "Fecha", "Cliente", "Total", "Pago", "Acciones")
        self.tree = ttk.Treeview(contenido, columns=columns, show="headings", height=20)
        for col in columns[:-1]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.heading("Acciones", text="Acciones")
        self.tree.column("Acciones", width=60, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.mostrar_icono_accion)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.orders = get_all_orders_with_user()
        for order in self.orders:
            self.tree.insert("", "end", values=(
                order["id"],
                order["created_at"],
                order["cliente"],
                f"S/. {order['total']:.2f}",
                order["payment_method"],
                "⋮"  # Ícono solo en la fila, no en header
            ))

    def mostrar_icono_accion(self, event):
        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if not row_id or col != '#6':  # columna "Acciones"
            return

        item_values = self.tree.item(row_id, "values")
        order_id = item_values[0]
        DetallePedidoView(self.master, order_id)

    def exportar_excel(self):
        try:
            export_dir = os.path.join(os.getcwd(), "resources")
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            df = pd.DataFrame(self.orders)
            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ventas_exportadas_{fecha_actual}.xlsx"
            save_path = os.path.join(export_dir, filename)

            df.to_excel(save_path, index=False)
            messagebox.showinfo("✅ Exportación exitosa", f"Ventas exportadas a:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_xml(self):
        try:
            export_dir = os.path.join(os.getcwd(), "resources")
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            root = ET.Element("Ventas")
            for o in self.orders:
                venta = ET.SubElement(root, "Venta")
                for key, value in o.items():
                    ET.SubElement(venta, key).text = str(value)

            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ventas_exportadas_{fecha_actual}.xml"
            save_path = os.path.join(export_dir, filename)

            tree = ET.ElementTree(root)
            tree.write(save_path, encoding="utf-8", xml_declaration=True)

            messagebox.showinfo("✅ XML exportado", f"Ventas exportadas a:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def navigate_logout(self):
        self.navigate("logout")
