import customtkinter as ctk
from tkinter import messagebox
from services.product_service import update_product, delete_product

class EditarProductoView(ctk.CTkFrame):
    def __init__(self, master, producto, on_success=None):
        super().__init__(master)
        self.master = master
        self.producto = producto  # objeto con atributos: id, name, price, unit, stock
        self.on_success = on_success
        self.configure(fg_color="white")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Editar Producto",
            font=("Segoe UI", 20, "bold"),
            text_color="#1a8341"
        ).pack(pady=10)

        # Campos del formulario
        self.entries = {}

        campos = [
            ("Nombre", self.producto.name),
            ("Precio", str(self.producto.price)),
            ("Unidad de medida", self.producto.unit),
            ("Stock", str(self.producto.stock)),
        ]

        for label, valor in campos:
            ctk.CTkLabel(self, text=label).pack(anchor="w", padx=10, pady=(10, 0))
            entry = ctk.CTkEntry(self)
            entry.insert(0, valor)
            entry.pack(fill="x", padx=10)
            self.entries[label] = entry

        # Botones de acción
        botones_frame = ctk.CTkFrame(self, fg_color="white")
        botones_frame.pack(pady=20)

        ctk.CTkButton(
            botones_frame,
            text="Guardar cambios",
            fg_color="#1a8341",
            hover_color="#157d35",
            command=self.guardar_cambios
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botones_frame,
            text="🗑️ Eliminar producto",
            fg_color="#ff4d4d",
            hover_color="#cc0000",
            command=self.eliminar_producto
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#bbbbbb",
            hover_color="#999999",
            command=self.master.destroy
        ).pack(pady=5)

    def guardar_cambios(self):
        try:
            name = self.entries["Nombre"].get()
            price = float(self.entries["Precio"].get())
            unit = self.entries["Unidad de medida"].get()
            stock = int(self.entries["Stock"].get())

            update_product(self.producto.id, name, price, unit, stock)

            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            if self.on_success:
                self.on_success()
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{e}")

    def eliminar_producto(self):
        confirm = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar este producto?")
        if not confirm:
            return

        try:
            delete_product(self.producto.id)
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
            if self.on_success:
                self.on_success()
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")
