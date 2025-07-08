import customtkinter as ctk
from tkinter import messagebox, filedialog
from services.product_service import add_product
import os

class AgregarProductoView(ctk.CTkFrame):
    def __init__(self, master, usuario_id=4, on_success=None):
        super().__init__(master)
        self.master = master
        self.usuario_id = usuario_id
        self.on_success = on_success
        self.image_path = ""  # Ruta de imagen seleccionada
        self.configure(fg_color="white")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Agregar Nuevo Producto",
            font=("Segoe UI", 20, "bold"),
            text_color="#1a8341"
        ).pack(pady=10)

        campos = [
            ("Nombre", ctk.CTkEntry),
            ("Precio", ctk.CTkEntry),
            ("Unidad de medida", ctk.CTkEntry),
            ("Stock", ctk.CTkEntry)
        ]

        self.inputs = {}

        for label_text, widget_type in campos:
            ctk.CTkLabel(self, text=label_text).pack(anchor="w", padx=10, pady=(10, 0))
            widget = widget_type(self)
            widget.pack(fill="x", padx=10)
            self.inputs[label_text] = widget

        # Selector de imagen
        ctk.CTkLabel(self, text="Imagen").pack(anchor="w", padx=10, pady=(10, 0))
        self.image_label = ctk.CTkLabel(self, text="Ningún archivo seleccionado", text_color="gray")
        self.image_label.pack(anchor="w", padx=10)
        ctk.CTkButton(
            self,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen,
            fg_color="#dddddd",
            text_color="black"
        ).pack(padx=10, pady=5, anchor="w")

        # Botones
        ctk.CTkButton(
            self,
            text="Guardar",
            height=40,
            fg_color="#1a8341",
            hover_color="#157d35",
            command=self.guardar_producto
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Cancelar",
            height=40,
            fg_color="#bbbbbb",
            hover_color="#999999",
            command=self.master.destroy
        ).pack()

    def seleccionar_imagen(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            file_name = os.path.basename(file_path)
            self.image_label.configure(text=file_name, text_color="black")

    def guardar_producto(self):
        try:
            name = self.inputs["Nombre"].get()
            price = float(self.inputs["Precio"].get())
            unit = self.inputs["Unidad de medida"].get()
            stock = int(self.inputs["Stock"].get())
            image_url = self.image_path  # Usar ruta completa seleccionada

            if not name or not unit or not image_url:
                messagebox.showwarning("Campos incompletos", "Completa todos los campos obligatorios.")
                return

            add_product(name, price, unit, stock, image_url, usuario_id=self.usuario_id)

            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            if self.on_success:
                self.on_success()
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")
