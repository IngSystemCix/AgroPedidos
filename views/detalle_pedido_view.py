import tkinter as tk
from tkinter import ttk

class DetallePedidoView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Detalle del Pedido", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Producto", "Cantidad", "Precio Unitario", "Subtotal"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Label(self, text="Estado del Pedido: Confirmado").pack(pady=10)
        tk.Button(self, text="Volver").pack(pady=5)
