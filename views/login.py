from PIL import Image
import customtkinter as ctk
from services.auth_service import authenticate
from views.product_catalog import ProductCatalogView
from views.admin_main import AdminMainApp

class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="#f3fdf2")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Iniciar Sesión")
        self.master.geometry("800x700")

        image_path = "./resources/images/logo.png"
        img = Image.open(image_path)
        resized_img = ctk.CTkImage(dark_image=img, light_image=img, size=(100, 100))

        wrapper = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=15)
        wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        padded_content = ctk.CTkFrame(wrapper, fg_color="transparent")
        padded_content.pack(padx=40, pady=40, fill="both")

        logo = ctk.CTkLabel(padded_content, image=resized_img, text="")
        logo.pack(pady=(0, 20))

        title = ctk.CTkLabel(
            padded_content,
            text="Iniciar Sesión",
            text_color="#1a8341",
            font=("Segoe UI", 24, "bold"),
        )
        title.pack(pady=(0, 20), fill="x")

        user_label = ctk.CTkLabel(padded_content, text="Usuario", text_color="#1a8341", font=("Segoe UI", 16, "bold"), anchor="w")
        user_label.pack(pady=(0, 5), fill="x")
        self.user_entry = ctk.CTkEntry(padded_content, placeholder_text="Usuario", height=50, corner_radius=10, width=300, font=("Segoe UI", 16))
        self.user_entry.pack(pady=10, fill="x", expand=True)

        pass_label = ctk.CTkLabel(padded_content, text="Contraseña", text_color="#1a8341", font=("Segoe UI", 16, "bold"), anchor="w")
        pass_label.pack(pady=(0, 5), fill="x")
        self.pass_entry = ctk.CTkEntry(padded_content, placeholder_text="Contraseña", show="*", height=50, corner_radius=10, width=300, font=("Segoe UI", 16))
        self.pass_entry.pack(pady=10, fill="x", expand=True)

        login_btn = ctk.CTkButton(padded_content, text="Iniciar Sesión", height=50, corner_radius=10, width=300, command=self.login, font=("Segoe UI", 16, "bold"))
        login_btn.pack(pady=10, fill="x", expand=True)

        register_btn = ctk.CTkButton(padded_content, text="Registrarse", height=50, corner_radius=10, fg_color="gray", hover_color="darkgray", width=300, font=("Segoe UI", 16, "bold"))
        register_btn.pack(pady=5, fill="x", expand=True)

        exit_btn = ctk.CTkButton(padded_content, text="Salir", height=50, corner_radius=10, fg_color="red", hover_color="darkred", width=300, command=self.master.quit, font=("Segoe UI", 16, "bold"))
        exit_btn.pack(pady=5, fill="x", expand=True)

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        user = authenticate(username, password)

        if user:
            print(f"✅ Usuario autenticado: {user.username} ({user.rol})")
            self.destroy()

            if user.rol == "Cliente":
                view = ProductCatalogView(master=self.master, usuario=user, logout_callback=self.logout)
            else:
                view = AdminMainApp(master=self.master, usuario=user, logout_callback=self.logout)

            view.pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(self, text="❌ Credenciales inválidas", text_color="red", font=("Segoe UI", 14, "bold")).pack(pady=10)

    def logout(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        LoginView(master=self.master).pack(fill="both", expand=True)
