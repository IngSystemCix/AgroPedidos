import customtkinter as ctk
from tkinter import messagebox
from services.auth_service import create_usuario

class RegisterView(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registro de Cliente")
        self.geometry("400x400")
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.grab_set()  # Bloquea la ventana principal hasta cerrar esta

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Registro de Usuario", font=("Segoe UI", 20, "bold"), text_color="#1a8341").pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nombre de usuario", width=300)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=300)
        self.password_entry.pack(pady=10)

        self.confirm_entry = ctk.CTkEntry(self, placeholder_text="Confirmar contraseña", show="*", width=300)
        self.confirm_entry.pack(pady=10)

        register_btn = ctk.CTkButton(self, text="Registrarse", command=self.register_user, height=40)
        register_btn.pack(pady=20)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return

        user = create_usuario(username, password, rol="Cliente")

        if user:
            messagebox.showinfo("Registro exitoso", "Cuenta creada correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")
