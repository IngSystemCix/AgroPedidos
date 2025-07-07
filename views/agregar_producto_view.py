import customtkinter as ctk
from tkinter import messagebox
from services.product_service import add_product

class AgregarProductoView(ctk.CTkFrame):
    def __init__(self, master, usuario_id=4, on_success=None):
        super().__init__(master)
        self.master = master
        self.usuario_id = usuario_id  # ID del usuario administrador
        self.on_success = on_success  # callback para recargar tabla
        self.configure(fg_color="white")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Título
        ctk.CTkLabel(
            self,
            text="Agregar Nuevo Producto",
            font=("Segoe UI", 20, "bold"),
            text_color="#1a8341"
        ).pack(pady=10)

        # Entradas
        campos = [
            ("Nombre", ctk.CTkEntry),
            ("Precio", ctk.CTkEntry),
            ("Unidad de medida", ctk.CTkEntry),
            ("Stock", ctk.CTkEntry),
            ("Imagen (ej: tomate.jpg)", ctk.CTkEntry)
        ]

        self.inputs = {}

        for label_text, widget_type in campos:
            ctk.CTkLabel(self, text=label_text).pack(anchor="w", padx=10, pady=(10, 0))
            widget = widget_type(self)
            widget.pack(fill="x", padx=10)
            self.inputs[label_text] = widget

        # Botón Guardar
        ctk.CTkButton(
            self,
            text="Guardar",
            height=40,
            fg_color="#1a8341",
            hover_color="#157d35",
            command=self.guardar_producto
        ).pack(pady=20)

        # Botón Cancelar
        ctk.CTkButton(
            self,
            text="Cancelar",
            height=40,
            fg_color="#bbbbbb",
            hover_color="#999999",
            command=self.master.destroy
        ).pack()

    def guardar_producto(self):
        try:
            name = self.inputs["Nombre"].get()
            price = float(self.inputs["Precio"].get())
            unit = self.inputs["Unidad de medida"].get()
            stock = int(self.inputs["Stock"].get())
            image_url = self.inputs["Imagen (ej: tomate.jpg)"].get()

            if not name or not unit or not image_url:
                messagebox.showwarning("Campos incompletos", "Completa todos los campos obligatorios.")
                return

            add_product(name, price, unit, stock, image_url, usuario_id=self.usuario_id)

            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            if self.on_success:
                self.on_success()  # Recarga tabla
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")
