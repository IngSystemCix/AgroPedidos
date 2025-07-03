import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import customtkinter as ctk
from views.login import LoginView  # Make sure LoginView inherits from ctk.CTkFrame

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # "dark" also works if you want dark mode
    ctk.set_default_color_theme("green")  # Change the primary color theme

    root = ctk.CTk()
    root.title("AgroPedidos")

    # White background
    root.configure(fg_color="white")

    # Set the window icon (optional)
    root.iconbitmap("./resources/images/favicon.ico")

    # Desired window size
    window_width = 800
    window_height = 700

    # Center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Load main view
    app = LoginView(master=root)
    app.pack(fill="both", expand=True)

    root.mainloop()
