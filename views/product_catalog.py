from PIL import Image
import customtkinter as ctk
from models import usuario
from services.product_service import get_all_products
import os
from datetime import datetime
import re
from functools import partial



class ProductCatalogView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.master = master
        self.usuario = usuario

        self.configure(fg_color="#f3fdf2")
        self.pack(fill="both", expand=True)
        self.create_widgets()

        self.carrito = []  # lista de tuplas (producto, cantidad)
        self.carrito_total = 0.0
        self.cart_button = None

    def create_widgets(self):
        # ---------------- HEADER ----------------
        header = ctk.CTkFrame(self, fg_color="#ffffff", height=80)
        header.pack(fill="x", side="top")

        # Logo
        logo_img = Image.open("./resources/images/logo.png")
        logo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
        ctk.CTkLabel(header, image=logo, text="").pack(side="left", padx=10, pady=10)

        # Título
        ctk.CTkLabel(
            header,
            text="AGROPEDIDOS",
            font=("Segoe UI", 28, "bold"),
            text_color="#1a8341",
        ).pack(side="left", padx=10)

        # Usuario
        user_icon = ctk.CTkLabel(header, text="👤", font=("Segoe UI", 18))
        user_icon.pack(side="right", padx=10)
        ctk.CTkLabel(header, text=self.usuario.username, font=("Segoe UI", 16)).pack(
            side="right", padx=(0, 10)
        )

        # ---------------- BUSCADOR ----------------
        search_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        search_frame.pack(pady=10)

        # Entrada de búsqueda
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar producto...", width=400, height=40
        )
        self.search_entry.pack(side="left", padx=(10, 0), pady=5)
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

        # Botón de búsqueda con ícono
        self.search_button = ctk.CTkButton(
            search_frame,
            text="🔍",  # o usa una imagen si tienes
            width=50,
            height=40,
            font=("Segoe UI", 18),
            command=self.perform_search,
        )
        self.search_button.pack(side="left", padx=10, pady=5)

        # ---------------- CARDS DE PRODUCTOS ----------------
        # Scroll vertical
        canvas_frame = ctk.CTkFrame(self, fg_color="#f3fdf2")
        canvas_frame.pack(fill="both", expand=True, pady=10)

        canvas = ctk.CTkCanvas(canvas_frame, bg="#f3fdf2", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Bind del scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(-int(event.delta / 120), "units")

        # Bind del scroll (Windows y Mac)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollbar = ctk.CTkScrollbar(
            canvas_frame, orientation="vertical", command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que contiene los productos en grid
        self.products_frame = ctk.CTkFrame(canvas, fg_color="#f3fdf2")
        self.products_window = canvas.create_window(
            (0, 0), window=self.products_frame, anchor="nw"
        )

        # Ajustar scroll al contenido
        self.products_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.products_frame.bind("<Configure>", self.on_resize)
        self.current_columns = None  # Para evitar renders innecesarios
        self.load_products()

        def on_canvas_resize(event):
            canvas.itemconfig(self.products_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_resize)

    def load_products(self, columns=None):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        if columns is None:
            columns = self.current_columns or 4

        products = get_all_products()

        for index, product in enumerate(products):
            row = index // columns
            col = index % columns
            self.create_product_card(product, row, col)

    def on_resize(self, event):
        container_width = self.products_frame.winfo_width()
        card_width = 150 + 30  # card + padding
        columns = max(1, container_width // card_width)

        if columns != self.current_columns:
            self.current_columns = columns
            self.load_products(columns)

    def perform_search(self):
        search_term = self.search_entry.get().lower()

        if not search_term:
            self.load_products(self.current_columns)  # si está vacío, carga todo
            return

        all_products = get_all_products()
        filtered_products = [p for p in all_products if search_term in p.name.lower()]

        for widget in self.products_frame.winfo_children():
            widget.destroy()

        columns = self.current_columns or 4
        for index, product in enumerate(filtered_products):
            row = index // columns
            col = index % columns
            self.create_product_card(product, row, col)

    def get_product_image(self, product):
        try:
            # Si en la base solo guardas "tomate.jpg", arma la ruta completa
            image_path = os.path.join("resources", "images", product.image_url)

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

            img = Image.open(image_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
        except Exception as e:
            print(f"[⚠] Error cargando imagen de '{product.name}': {e}")
            return None

    def create_product_card(self, product, row, col):
        card = ctk.CTkFrame(
            self.products_frame,
            corner_radius=12,
            fg_color="#ffffff",
            width=150,
            height=300,
        )
        card.grid(row=row, column=col, padx=15, pady=15)
        card.grid_propagate(
            False
        )  # opcional: evita que el contenido modifique el tamaño del card

        image = self.get_product_image(product)
        if image:
            ctk.CTkLabel(card, image=image, text="").pack(pady=(10, 5))
        else:
            ctk.CTkLabel(card, text="Sin imagen", font=("Arial", 12, "italic")).pack()

        # Nombre del producto
        ctk.CTkLabel(
            card, text=product.name, font=("Segoe UI", 16, "bold"), text_color="#1a8341"
        ).pack()

        # Precio
        price_text = f"S/ {product.price:.2f}"
        ctk.CTkLabel(
            card, text=price_text, font=("Segoe UI", 18, "bold"), text_color="#1a8341"
        ).pack()

        # Unidad de medida
        unidad = getattr(
            product, "unit", "por unidad"
        )  # si tienes campo 'unit' en Product
        ctk.CTkLabel(
            card,
            text=unidad,
            font=("Segoe UI", 12, "bold"),
            text_color="#b05c1e",
            fg_color="#fef3c7",
        ).pack(pady=(0, 5))

        # Selector de cantidad
        qty_frame = ctk.CTkFrame(card, fg_color="transparent")
        qty_frame.pack(pady=5)

        # Cantidad inicial
        product._qty_var = ctk.StringVar(value="1")

        def decrease_qty():
            val = int(product._qty_var.get())
            if val > 1:
                product._qty_var.set(str(val - 1))

        def increase_qty():
            val = int(product._qty_var.get())
            product._qty_var.set(str(val + 1))

        ctk.CTkButton(qty_frame, text="-", width=30, command=decrease_qty).pack(
            side="left", padx=5
        )
        ctk.CTkLabel(qty_frame, textvariable=product._qty_var, width=30).pack(
            side="left"
        )
        ctk.CTkButton(qty_frame, text="+", width=30, command=increase_qty).pack(
            side="left", padx=5
        )

        # Botón Agregar al carrito
        ctk.CTkButton(
            card,
            text="🛒 Agregar al carrito",
            font=("Segoe UI", 14, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            command=lambda p=product: self.agregar_al_carrito(p, int(p._qty_var.get())),
        ).pack(pady=(10, 0), padx=10, fill="x")

    def agregar_al_carrito(self, producto, cantidad):
        # Verificar si ya está en el carrito
        for i, (p, c) in enumerate(self.carrito):
            if p.id == producto.id:
                self.carrito[i] = (p, c + cantidad)
                break
        else:
            self.carrito.append((producto, cantidad))

        # Actualizar total
        self.carrito_total += float(producto.price) * cantidad
        self.mostrar_boton_carrito()

    def mostrar_boton_carrito(self):
        texto = f"🛒 Ver carrito - S/ {self.carrito_total:.2f}"

        if self.cart_button:
            self.cart_button.configure(text=texto)
            return

        self.cart_button = ctk.CTkButton(
            self,
            text=texto,
            font=("Segoe UI", 16, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            corner_radius=20,
            command=self.abrir_carrito,
        )
        self.cart_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)


    def abrir_carrito(self):
        if not self.carrito:
            ctk.CTkMessagebox(
                title="Carrito vacío",
                message="No hay productos en el carrito.",
                icon="info",
            )
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("🛒 Carrito de Compras")
        ventana.geometry("550x650")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="🛒 Carrito de Compras",
            font=("Segoe UI", 20, "bold"),
            text_color="#1a8341",
        ).pack(pady=15)

        # Frame para productos
        lista_frame = ctk.CTkFrame(ventana, fg_color="#ffffff")
        lista_frame.pack(fill="both", expand=False, padx=20, pady=(0, 10))

        # Controlar totales
        total_var = ctk.StringVar(value=f"{self.carrito_total:.2f}")

        # Mostrar productos
        for i, (producto, cantidad) in enumerate(self.carrito):
            frame = ctk.CTkFrame(lista_frame, fg_color="transparent")
            frame.pack(fill="x", pady=5)

            qty_var = ctk.IntVar(value=cantidad)
            subtotal_var = ctk.StringVar(value=f"S/ {float(producto.price) * cantidad:.2f}")

            def actualizar_total(prod, qvar, s_var):
                new_qty = qvar.get()
                self.carrito[i] = (prod, new_qty)
                new_subtotal = float(prod.price) * new_qty
                s_var.set(f"S/ {new_subtotal:.2f}")

                nuevo_total = sum(float(p.price) * c for p, c in self.carrito)
                total_var.set(f"{nuevo_total:.2f}")

            # Etiqueta de nombre
            ctk.CTkLabel(frame, text=producto.name, font=("Segoe UI", 14)).pack(side="left", padx=10)

            # Subtotal individual
            ctk.CTkLabel(frame, textvariable=subtotal_var, font=("Segoe UI", 14), text_color="#1a8341").pack(side="right", padx=15)

            # Botones de cantidad
            ctk.CTkButton(frame, text="-", width=30,
                command=partial(lambda v, p, q, s: (v.set(max(1, v.get() - 1)), actualizar_total(p, v, s)),
                                qty_var, producto, qty_var, subtotal_var)
            ).pack(side="right", padx=2)

            ctk.CTkLabel(frame, textvariable=qty_var, width=30).pack(side="right")

            ctk.CTkButton(frame, text="+", width=30,
                command=partial(lambda v, p, q, s: (v.set(v.get() + 1), actualizar_total(p, v, s)),
                                qty_var, producto, qty_var, subtotal_var)
            ).pack(side="right", padx=2)


        # Total general
        ctk.CTkLabel(ventana, text="Total general:", font=("Segoe UI", 16)).pack(
            pady=(10, 0)
        )
        total_label = ctk.CTkLabel(
            ventana,
            textvariable=total_var,
            font=("Segoe UI", 20, "bold"),
            text_color="#1a8341",
        )
        total_label.pack(pady=5)

        # Método de pago
        ctk.CTkLabel(ventana, text="Método de pago:", font=("Segoe UI", 16, "bold")).pack(
            pady=(10, 5)
        )
        metodo_pago = ctk.StringVar(value="Tarjeta")

        metodo_selector = ctk.CTkSegmentedButton(
            ventana, values=["Tarjeta", "Yape"], variable=metodo_pago
        )
        metodo_selector.pack(pady=5)

        # Frame para inputs dinámicos
        pago_frame = ctk.CTkFrame(ventana, fg_color="transparent")
        pago_frame.pack(pady=10, fill="x", padx=20)

        tarjeta_inputs = {}
        yape_inputs = {}

        def render_inputs(*args):
            for widget in pago_frame.winfo_children():
                widget.destroy()

            if metodo_pago.get() == "Tarjeta":
                tarjeta_inputs.clear()

                tarjeta_inputs["numero"] = ctk.CTkEntry(
                    pago_frame, placeholder_text="Número de tarjeta (16 dígitos)"
                )
                tarjeta_inputs["numero"].pack(pady=5, fill="x")

                tarjeta_inputs["fecha"] = ctk.CTkEntry(
                    pago_frame, placeholder_text="Fecha de vencimiento (MM/AA)"
                )
                tarjeta_inputs["fecha"].pack(pady=5, fill="x")

                tarjeta_inputs["cvv"] = ctk.CTkEntry(
                    pago_frame, placeholder_text="CVV (3 dígitos)", show="*"
                )
                tarjeta_inputs["cvv"].pack(pady=5, fill="x")

            else:
                yape_inputs.clear()

                yape_inputs["numero"] = ctk.CTkEntry(
                    pago_frame, placeholder_text="Número celular (9 dígitos)"
                )
                yape_inputs["numero"].pack(pady=5, fill="x")

                yape_inputs["codigo"] = ctk.CTkEntry(
                    pago_frame, placeholder_text="Código de aprobación (6 dígitos)"
                )
                yape_inputs["codigo"].pack(pady=5, fill="x")

        metodo_pago.trace_add("write", render_inputs)
        render_inputs()

        # Función para validar y realizar pedido
        def realizar_pedido():
            if metodo_pago.get() == "Tarjeta":
                num = tarjeta_inputs["numero"].get()
                fecha = tarjeta_inputs["fecha"].get()
                cvv = tarjeta_inputs["cvv"].get()

                if not (num.isdigit() and len(num) == 16):
                    ctk.CTkMessagebox(
                        title="Error", message="Número de tarjeta inválido", icon="cancel"
                    )
                    return

                try:
                    mes, anio = map(int, fecha.split("/"))
                    hoy = datetime.now()
                    vencimiento = datetime(int("20" + str(anio)), mes, 1)
                    if vencimiento < hoy:
                        raise ValueError
                except:
                    ctk.CTkMessagebox(
                        title="Error",
                        message="Fecha de vencimiento inválida",
                        icon="cancel",
                    )
                    return

                if not (cvv.isdigit() and len(cvv) == 3):
                    ctk.CTkMessagebox(title="Error", message="CVV inválido", icon="cancel")
                    return

            else:
                numero = yape_inputs["numero"].get()
                codigo = yape_inputs["codigo"].get()

                if not (numero.isdigit() and len(numero) == 9):
                    ctk.CTkMessagebox(
                        title="Error", message="Número Yape inválido", icon="cancel"
                    )
                    return

                if not (codigo.isdigit() and len(codigo) == 6):
                    ctk.CTkMessagebox(
                        title="Error", message="Código Yape inválido", icon="cancel"
                    )
                    return

            # Aquí podrías guardar el pedido en la BD
            total = total_var.get()
            ctk.CTkMessagebox(
                title="Pedido exitoso",
                message=f"Tu pedido fue realizado con éxito.\nTotal: S/ {total}",
                icon="check",
            )
            ventana.destroy()

        # Botón Realizar pedido
        ctk.CTkButton(
            ventana,
            textvariable=ctk.StringVar(value=f"🛒 Realizar pedido - S/ {total_var.get()}"),
            font=("Segoe UI", 16, "bold"),
            fg_color="#1a8341",
            hover_color="#146c34",
            command=realizar_pedido,
        ).pack(pady=20, fill="x", padx=20)
