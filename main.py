import tkinter as ttk
from views.login import LoginView

if __name__ == "__main__":
    root = ttk.Tk()
    root.title("AgroPedidos")

    # Tamaño de la ventana
    ancho_ventana = 800
    alto_ventana = 600

    # Obtener tamaño de pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    # Calcular posición x, y para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Posicionar y dar tamaño a la ventana
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    # Iniciar vista
    app = LoginView(master=root)
    app.pack(fill=ttk.BOTH, expand=True)

    root.mainloop()
