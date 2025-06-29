from PIL import Image
import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="#f3fdf2")  # Fondo general
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Iniciar Sesión")
        self.master.geometry("800x700")

        image_path = "./resources/images/logo.png"  # Cambia a tu ruta real
        img = Image.open(image_path)
        resized_img = ctk.CTkImage(dark_image=img, light_image=img, size=(100, 100))

        # Contenedor principal centrado, tamaño adaptable
        wrapper = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=15)
        wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        # Subcontenedor con padding interno, que se adapta al contenido
        padded_content = ctk.CTkFrame(wrapper, fg_color="transparent")
        padded_content.pack(padx=40, pady=40, fill="both")

        # Logo
        logo = ctk.CTkLabel(padded_content, image=resized_img, text="")
        logo.pack(pady=(0, 20))

        # Título
        title = ctk.CTkLabel(padded_content, text="Iniciar Sesión", text_color="#1a8341", font=("Segoe UI", 24, "bold"))
        title.pack(pady=(0, 20), fill="x")

        # Usuario
        user_label = ctk.CTkLabel(padded_content, text="Usuario", text_color="#1a8341", font=("Segoe UI", 16, "bold"), anchor="w")
        user_label.pack(pady=(0, 5), fill="x")
        self.user_entry = ctk.CTkEntry(padded_content, placeholder_text="Usuario", height=50, corner_radius=10, width=300,font=("Segoe UI", 16))
        self.user_entry.pack(pady=10, fill="x", expand=True)

        # Contraseña
        pass_label = ctk.CTkLabel(padded_content, text="Contraseña", text_color="#1a8341", font=("Segoe UI", 16, "bold"), anchor="w")
        pass_label.pack(pady=(0, 5), fill="x")
        self.pass_entry = ctk.CTkEntry(padded_content, placeholder_text="Contraseña", show="*", height=50, corner_radius=10, width=300,font=("Segoe UI", 16))
        self.pass_entry.pack(pady=10, fill="x", expand=True)

        # Botón Iniciar Sesión
        login_btn = ctk.CTkButton(padded_content, text="Iniciar Sesión", height=50, corner_radius=10, width=300, command=self.login, font=("Segoe UI", 16, "bold"))
        login_btn.pack(pady=10, fill="x", expand=True)

        # Botón Registrarse
        register_btn = ctk.CTkButton(padded_content, text="Registrarse", height=50, corner_radius=10,
                                     fg_color="gray", hover_color="darkgray", width=300, command=self.register, font=("Segoe UI", 16, "bold"))
        register_btn.pack(pady=5, fill="x", expand=True)

        # Botón Salir
        exit_btn = ctk.CTkButton(padded_content, text="Salir", height=50, corner_radius=10,
                                 fg_color="red", hover_color="darkred", width=300, command=self.master.quit, font=("Segoe UI", 16, "bold"))
        exit_btn.pack(pady=5, fill="x", expand=True)

    def login(self):
        print(f"Iniciar sesión con usuario: {self.user_entry.get()}")

    def register(self):
        print("Abrir registro...")
