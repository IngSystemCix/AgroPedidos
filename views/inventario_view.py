import tkinter as tk
from tkinter import ttk

class InventarioView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Inventario", font=("Arial", 16, "bold")).pack(pady=10)

        search = tk.Frame(self)
        search.pack(pady=5)
        tk.Label(search, text="Buscar:").pack(side="left")
        tk.Entry(search).pack(side="left", padx=5)

        tk.Button(search, text="Actualizar").pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Stock", "Precio"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, pady=10)
