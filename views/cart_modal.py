
from customtkinter import *
from datetime import datetime
from tkinter import messagebox
import mysql.connector

class CartModal(CTkToplevel):
    def __init__(self, master, carrito, total, reset_callback, usuario):
        super().__init__(master)
        self.title("🛒 Carrito de Compras")
        self.geometry("600x650")
        self.carrito = carrito
        self.total = total
        self.reset_callback = reset_callback
        self.usuario = usuario
        self.grab_set()

        self.total_var = StringVar(value=f"{self.total:.2f}")
        self.metodo_pago = StringVar(value="Tarjeta")
        self.tarjeta_inputs = {}
        self.yape_inputs = {}

        self.render_ui()

    def render_ui(self):
        CTkLabel(self, text="🛒 Carrito de Compras", font=("Segoe UI", 20, "bold"), text_color="#1a8341").pack(pady=15)

        self.lista_frame = CTkFrame(self, fg_color="#ffffff")
        self.lista_frame.pack(fill="both", expand=False, padx=20, pady=(0, 10))

        self.render_items()

        CTkLabel(self, text="Total general:", font=("Segoe UI", 16)).pack(pady=(10, 0))
        CTkLabel(self, textvariable=self.total_var, font=("Segoe UI", 20, "bold"), text_color="#1a8341").pack(pady=5)

        CTkLabel(self, text="Método de pago:", font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        CTkSegmentedButton(self, values=["Tarjeta", "Yape"], variable=self.metodo_pago, command=self.render_inputs).pack(pady=5)

        self.pago_frame = CTkFrame(self, fg_color="transparent")
        self.pago_frame.pack(pady=10, fill="x", padx=20)
        self.render_inputs()

        CTkButton(
            self,
            text=f"🛒 Realizar pedido - S/ {self.total_var.get()}",
            font=("Segoe UI", 16, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            command=self.realizar_pedido
        ).pack(pady=20, fill="x", padx=20)

    def render_items(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        for producto, cantidad in self.carrito:
            item_frame = CTkFrame(self.lista_frame, fg_color="#f1f1f1", corner_radius=10)
            item_frame.pack(fill="x", pady=5, padx=5)

            CTkLabel(item_frame, text=producto.name, font=("Segoe UI", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            CTkLabel(item_frame, text=f"S/ {float(producto.price):.2f}", font=("Segoe UI", 14), text_color="#1a8341").grid(row=0, column=1, sticky="e", padx=10)

            CTkButton(item_frame, text="-", width=30, command=lambda p=producto: self.cambiar_cantidad(p, -1)).grid(row=1, column=0, padx=5, pady=5)
            CTkLabel(item_frame, text=f"Cantidad: {cantidad}", font=("Segoe UI", 14)).grid(row=1, column=1, padx=5)
            CTkButton(item_frame, text="+", width=30, command=lambda p=producto: self.cambiar_cantidad(p, 1)).grid(row=1, column=2, padx=5)
            CTkButton(item_frame, text="🗑️ Quitar", fg_color="#30c88f", command=lambda p=producto: self.quitar_producto(p)).grid(row=1, column=3, padx=10)

    def cambiar_cantidad(self, producto, delta):
        for i, (p, c) in enumerate(self.carrito):
            if p.id == producto.id:
                nueva_cantidad = c + delta
                if nueva_cantidad <= 0:
                    del self.carrito[i]
                else:
                    self.carrito[i] = (p, nueva_cantidad)
                break
        self.actualizar_total()
        self.render_items()

    def quitar_producto(self, producto):
        self.carrito = [(p, c) for p, c in self.carrito if p.id != producto.id]
        self.actualizar_total()
        self.render_items()

    def actualizar_total(self):
        self.total = sum(float(p.price) * c for p, c in self.carrito)
        self.total_var.set(f"{self.total:.2f}")

    def render_inputs(self, *_):
        for widget in self.pago_frame.winfo_children():
            widget.destroy()

        if self.metodo_pago.get() == "Tarjeta":
            self.tarjeta_inputs.clear()
            self.tarjeta_inputs["numero"] = CTkEntry(self.pago_frame, placeholder_text="Número de tarjeta (16 dígitos)")
            self.tarjeta_inputs["numero"].pack(pady=5, fill="x")
            self.tarjeta_inputs["fecha"] = CTkEntry(self.pago_frame, placeholder_text="Fecha de vencimiento (MM/AA)")
            self.tarjeta_inputs["fecha"].pack(pady=5, fill="x")
            self.tarjeta_inputs["cvv"] = CTkEntry(self.pago_frame, placeholder_text="CVV (3 dígitos)", show="*")
            self.tarjeta_inputs["cvv"].pack(pady=5, fill="x")
        else:
            self.yape_inputs.clear()
            self.yape_inputs["numero"] = CTkEntry(self.pago_frame, placeholder_text="Número celular (9 dígitos)")
            self.yape_inputs["numero"].pack(pady=5, fill="x")
            self.yape_inputs["codigo"] = CTkEntry(self.pago_frame, placeholder_text="Código de aprobación (6 dígitos)")
            self.yape_inputs["codigo"].pack(pady=5, fill="x")

    def validar_datos(self):
        if self.metodo_pago.get() == "Tarjeta":
            num = self.tarjeta_inputs["numero"].get()
            fecha = self.tarjeta_inputs["fecha"].get()
            cvv = self.tarjeta_inputs["cvv"].get()
            if not (num.isdigit() and len(num) == 16):
                messagebox.showerror("Error", "Número de tarjeta inválido")
                return False
            try:
                mes, anio = map(int, fecha.split("/"))
                hoy = datetime.now()
                vencimiento = datetime(int("20" + str(anio)), mes, 1)
                if vencimiento < hoy:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Fecha de vencimiento inválida")
                return False
            if not (cvv.isdigit() and len(cvv) == 3):
                messagebox.showerror("Error", "CVV inválido")
                return False
        else:
            numero = self.yape_inputs["numero"].get()
            codigo = self.yape_inputs["codigo"].get()
            if not (numero.isdigit() and len(numero) == 9):
                messagebox.showerror("Error", "Número Yape inválido")
                return False
            if not (codigo.isdigit() and len(codigo) == 6):
                messagebox.showerror("Error", "Código Yape inválido")
                return False
        return True

    def realizar_pedido(self):
        if not self.validar_datos() or not self.carrito:
            return
        if self.guardar_pedido():
            messagebox.showinfo("Pedido exitoso", f"Pedido registrado correctamente. Total: S/ {self.total_var.get()}")
            self.reset_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el pedido. Intenta nuevamente.")

    def guardar_pedido(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="agropedidos_db"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO `order` (usuario_id, created_at, total, payment_method) VALUES (%s, %s, %s, %s)",
                (self.usuario.id, datetime.now(), self.total, self.metodo_pago.get()))
            order_id = cursor.lastrowid

            for producto, cantidad in self.carrito:
                subtotal = float(producto.price) * cantidad
                cursor.execute("INSERT INTO orderitem (order_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                    (order_id, producto.id, cantidad, subtotal))

                # Descontar stock del producto
                cursor.execute("UPDATE product SET stock = stock - %s WHERE id = %s", (cantidad, producto.id))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"[❌] Error al guardar pedido: {e}")
            return False
