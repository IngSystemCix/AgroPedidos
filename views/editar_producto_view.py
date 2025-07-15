import customtkinter as ctk
from tkinter import messagebox, filedialog
from services.product_service import update_product, soft_delete_product
import os
import shutil
from config.connection import get_connection

class EditarProductoView(ctk.CTkFrame):
    def __init__(self, master, producto, on_success=None):
        super().__init__(master)
        self.master = master
        self.producto = producto
        self.on_success = on_success
        self.image_filename = producto.image_url if hasattr(producto, "image_url") else ""
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

        # Imagen
        ctk.CTkLabel(self, text="Imagen").pack(anchor="w", padx=10, pady=(10, 0))
        self.image_label = ctk.CTkLabel(
            self,
            text=self.image_filename if self.image_filename else "Ningún archivo seleccionado",
            text_color="black" if self.image_filename else "gray"
        )
        self.image_label.pack(anchor="w", padx=10)

        ctk.CTkButton(
            self,
            text="Seleccionar Imagen",
            command=self.seleccionar_imagen,
            fg_color="#dddddd",
            text_color="black"
        ).pack(padx=10, pady=5, anchor="w")

        # Botones
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

    def seleccionar_imagen(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            nombre_archivo = os.path.basename(file_path)
            destino_dir = os.path.join("resources", "images")
            os.makedirs(destino_dir, exist_ok=True)
            destino_path = os.path.join(destino_dir, nombre_archivo)

            if not os.path.exists(destino_path):
                shutil.copy(file_path, destino_path)

            self.image_filename = nombre_archivo
            self.image_label.configure(text=nombre_archivo, text_color="black")

    def guardar_cambios(self):
        try:
            name = self.entries["Nombre"].get().strip()
            price_str = self.entries["Precio"].get().strip()
            unit = self.entries["Unidad de medida"].get().strip()
            stock_str = self.entries["Stock"].get().strip()

            if not name or not unit:
                messagebox.showerror("Campo obligatorio", "Nombre y unidad de medida no pueden estar vacíos.")
                return

            price = float(price_str)
            stock = int(stock_str)

            if price < 0 or stock < 0:
                messagebox.showerror("Valor inválido", "El precio y el stock no pueden ser negativos.")
                return

            image_url = self.image_filename
            update_product(self.producto.id, name, price, unit, stock, image_url)

            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            if self.on_success:
                self.on_success()
            self.master.destroy()

        except ValueError:
            messagebox.showerror("Error de formato", "Verifica que el precio y el stock sean numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{e}")

    def eliminar_producto(self):
        confirm = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar este producto?")
        if not confirm:
            return

        try:
            if self.producto_tiene_historial_ventas():
                messagebox.showerror("Error", "No se puede eliminar este producto porque tiene historial de ventas.")
                return

            soft_delete_product(self.producto.id)
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
            if self.on_success:
                self.on_success()
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

    def producto_tiene_historial_ventas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orderitem WHERE product_id = %s", (self.producto.id,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
