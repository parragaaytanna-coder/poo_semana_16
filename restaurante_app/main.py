import tkinter as tk
from pathlib import Path

# Importación de servicios y vistas
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    def __init__(self):
        # Inicialización de la ventana principal
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Restaurante")
        self.root.geometry("920x560")
        self.root.minsize(780, 500)
        self.icono_app = None

        # Configuración de rutas y servicios
        ruta_base = Path(__file__).resolve().parent
        self.configurar_icono_ventana(ruta_base)

        # Instancia del servicio de archivos en la carpeta 'datos'
        archivo_servicio = ArchivoServicio(ruta_base / "datos")
        # Inyección del servicio de archivos en la lógica del restaurante
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual = None
        
        # Muestra la pantalla inicial de login
        self.mostrar_login()

    def configurar_icono_ventana(self, ruta_base):
        """Carga el icono de la ventana principal."""
        ruta_icono = ruta_base / "assets" / "logo" / "icono.png"
        if ruta_icono.exists():
            try:
                self.icono_app = tk.PhotoImage(file=str(ruta_icono))
                self.root.iconphoto(True, self.icono_app)
            except Exception:
                pass

    def limpiar_vista(self):
        """Limpia el frame actual antes de cambiar de pantalla."""
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def mostrar_login(self):
        """Muestra la vista de Login pasando master, restaurante_servicio y al_iniciar_sesion."""
        self.limpiar_vista()
        self.vista_actual = LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_principal
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_principal(self, usuario):
        """Muestra la vista principal cargando el servicio de restaurante."""
        self.limpiar_vista()
        self.vista_actual = MainView(
            self.root, 
            usuario, 
            self.restaurante_servicio,
            self.mostrar_login
        )
        self.vista_actual.pack(fill="both", expand=True)

    def iniciar(self):
        """Ejecuta el loop principal de la interfaz."""
        self.root.mainloop()


if __name__ == "__main__":
    app = AplicacionRestaurante()
    app.iniciar()