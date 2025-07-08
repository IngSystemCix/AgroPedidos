# views/components/search_bar.py
import customtkinter as ctk

class SearchBar:
    def __init__(self, master, search_callback):
        search_frame = ctk.CTkFrame(master, fg_color="#f3fdf2")
        search_frame.pack(pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar producto...", width=400, height=40
        )
        self.search_entry.pack(side="left", padx=(10, 0), pady=5)
        self.search_entry.bind("<Return>", lambda event: search_callback())

        self.search_button = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=50,
            height=40,
            font=("Segoe UI", 18),
            command=search_callback,
        )
        self.search_button.pack(side="left", padx=10, pady=5)
