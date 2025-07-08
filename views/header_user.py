# views/components/header_user.py
import customtkinter as ctk
from PIL import Image

class HeaderUser:
    def __init__(self, master, usuario, navigate):
        header = ctk.CTkFrame(master, fg_color="#ffffff", height=80)
        header.pack(fill="x", side="top")

        logo_img = Image.open("./resources/images/logo.png")
        logo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
        ctk.CTkLabel(header, image=logo, text="").pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(
            header,
            text="AGROPEDIDOS",
            font=("Segoe UI", 28, "bold"),
            text_color="#1a8341",
        ).pack(side="left", padx=10)

        user_section = ctk.CTkFrame(header, fg_color="transparent")
        user_section.pack(side="right", padx=20)
        ctk.CTkLabel(user_section, text="👤", font=("Segoe UI", 18)).pack(side="left", padx=5)
        ctk.CTkLabel(user_section, text=usuario.username, font=("Segoe UI", 16)).pack(side="left", padx=5)
        ctk.CTkButton(user_section, text="Cerrar sesión", width=120,
                      fg_color="#ff4d4d", hover_color="#cc0000",
                      command=lambda: navigate("logout")).pack(side="left", padx=5)
