from tkinter import ttk

class LoginView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(style="Main.TFrame")
        self.create_widgets()
        self.init_styles()

    def init_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=4)
        style.configure("TEntry", font=("Arial", 12), padding=4)
        style.configure("TFrame", background="#f0f0f0")

    def create_widgets(self):
        # Etiqueta de título
        self.title_label = ttk.Label(self, text="Iniciar Sesión", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # Campo de entrada para el nombre de usuario
        self.username_label = ttk.Label(self, text="Nombre de Usuario:")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        # Campo de entrada para la contraseña
        self.password_label = ttk.Label(self, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = ttk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=20)

        # Botón de registro
        self.register_button = ttk.Button(self, text="Registrarse", command=self.register)
        self.register_button.pack(pady=5)
        # Botón de salir
        self.exit_button = ttk.Button(self, text="Salir", command=self.master.quit)
        self.exit_button.pack(pady=5)
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Aquí iría la lógica de autenticación
        print(f"Intentando iniciar sesión con {username} y {password}")

    def register(self):
        print("Abrir ventana de registro")
