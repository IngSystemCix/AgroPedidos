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
        self.stock_invalido = False

        self.render_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def render_ui(self):
        self.content_frame = CTkScrollableFrame(self, fg_color="transparent", width=580, height=600)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        CTkLabel(self.content_frame, text="🛒 Carrito de Compras", font=("Segoe UI", 20, "bold"), text_color="#1a8341").pack(pady=15)

        self.lista_frame = CTkFrame(self.content_frame, fg_color="#ffffff")
        self.lista_frame.pack(fill="both", expand=False, padx=10, pady=(0, 10))

        self.render_items()

        CTkLabel(self.content_frame, text="Total general:", font=("Segoe UI", 16)).pack(pady=(10, 0))
        CTkLabel(self.content_frame, textvariable=self.total_var, font=("Segoe UI", 20, "bold"), text_color="#1a8341").pack(pady=5)

        CTkLabel(self.content_frame, text="Método de pago:", font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        CTkSegmentedButton(self.content_frame, values=["Tarjeta", "Yape"], variable=self.metodo_pago, command=self.render_inputs).pack(pady=5)

        self.pago_frame = CTkFrame(self.content_frame, fg_color="transparent")
        self.pago_frame.pack(pady=10, fill="x", padx=10)
        self.render_inputs()

        self.btn_realizar = CTkButton(
            self.content_frame,
            text=f"🛒 Realizar pedido - S/ {self.total_var.get()}",
            font=("Segoe UI", 16, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            command=self.realizar_pedido
        )
        self.btn_realizar.pack(pady=20, fill="x", padx=10)

        self.validar_stock_carrito()

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
                stock_actual = self.obtener_stock_actual(producto.id)
                if nueva_cantidad <= 0:
                    del self.carrito[i]
                elif nueva_cantidad <= stock_actual:
                    self.carrito[i] = (p, nueva_cantidad)
                break
        self.actualizar_total()
        self.render_items()
        self.validar_stock_carrito()

    def obtener_stock_actual(self, product_id):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="agropedidos_db"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM product WHERE id = %s", (product_id,))
            stock = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return stock
        except:
            return 0

    def quitar_producto(self, producto):
        self.carrito = [(p, c) for p, c in self.carrito if p.id != producto.id]
        self.actualizar_total()
        self.render_items()
        self.validar_stock_carrito()

    def actualizar_total(self):
        self.total = sum(float(p.price) * c for p, c in self.carrito)
        self.total_var.set(f"{self.total:.2f}")
        self.btn_realizar.configure(text=f"🛒 Realizar pedido - S/ {self.total_var.get()}")

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

    def validar_stock_carrito(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="agropedidos_db"
            )
            cursor = conn.cursor()
            self.stock_invalido = False

            for producto, cantidad in self.carrito:
                cursor.execute("SELECT stock FROM product WHERE id = %s", (producto.id,))
                stock = cursor.fetchone()
                if not stock or stock[0] < cantidad:
                    self.stock_invalido = True
                    break

            cursor.close()
            conn.close()

            if self.stock_invalido:
                self.btn_realizar.configure(state="disabled", text="❌ Stock insuficiente")
            else:
                self.btn_realizar.configure(state="normal", text=f"🛒 Realizar pedido - S/ {self.total_var.get()}")
        except Exception as e:
            print(f"[❌] Error al validar stock: {e}")
            self.btn_realizar.configure(state="disabled", text="❌ Error de stock")

    def realizar_pedido(self):
        if not self.validar_datos() or not self.carrito:
            return

        self.validar_stock_carrito()

        if self.stock_invalido:
            messagebox.showerror("Error de stock", "Uno o más productos no tienen suficiente stock disponible.")
            return

        if self.guardar_pedido():
            messagebox.showinfo("Pedido exitoso", f"Pedido registrado correctamente. Total: S/ {self.total_var.get()}")
            self.on_close()
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
                cursor.execute("UPDATE product SET stock = stock - %s WHERE id = %s", (cantidad, producto.id))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"[❌] Error al guardar pedido: {e}")
            return False

    def on_close(self):
        for producto, _ in self.carrito:
            if hasattr(producto, "_qty_var"):
                producto._qty_var.set("1")
        self.reset_callback()
        self.destroy()
