import customtkinter as ctk

class AdminPlaceholderView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        label = ctk.CTkLabel(self, text=f"Hola {usuario.username} 👋\nÁrea de administrador aún en construcción.")
        label.pack(padx=40, pady=40)
