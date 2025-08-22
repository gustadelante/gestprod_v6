import flet as ft
import os
import sys
from views.producto_turno import producto_turno_view
from views.etiqueta import etiqueta_view
from data.database import create_connection, create_table
from components.appbar import create_appbar  # Importar la AppBar

def get_app_dir() -> str:
    """Devuelve la carpeta donde está el ejecutable (.exe) o, en desarrollo, la carpeta del archivo actual."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # PyInstaller o flet pack (congelado)
        return os.path.dirname(sys.executable)
    # Desarrollo: usar la carpeta del archivo main.py
    return os.path.dirname(os.path.abspath(__file__))


# Rutas de archivos en la carpeta de la app/ejecutable
APP_DIR = get_app_dir()
# Ruta del archivo para guardar la preferencia del tema (no se usa para cambiar tema, pero mantenemos compatibilidad)
THEME_PREFERENCE_FILE = os.path.join(APP_DIR, "theme_preference.txt")
WINDOW_PREFERENCE_FILE = os.path.join(APP_DIR, "window_preference.txt")

def load_theme_preference():
    """Compatibilidad: se fuerza modo claro sin leer preferencia."""
    return "light"

def save_theme_preference(theme_mode):
    """Compatibilidad: no se guarda preferencia de tema (modo fijo claro)."""
    pass


def load_window_preference():
    """Cargar la preferencia de la ventana (maximizada o normal)."""
    try:
        with open(WINDOW_PREFERENCE_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "normal"


def save_window_preference(state: str):
    """Guardar la preferencia de la ventana en el archivo. state: 'maximized'|'normal'"""
    with open(WINDOW_PREFERENCE_FILE, "w") as file:
        file.write(state)



def main(page: ft.Page):
       
    # Configuración de la página    
    # Forzar modo claro y deshabilitar cambio de tema
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Establecer el tamaño y posición de la ventana
    page.window.title_bar_hidden = False  # Asegura que la barra de título del SO sea visible
    page.window.title_bar_buttons_hidden = False  # Asegura que los botones (min/max/cerrar) sean visibles
    page.window.resizable = True
    # Aplicar preferencia de ventana
    window_pref = load_window_preference()
    page.window.maximized = True if window_pref == "maximized" else False
    page.window.always_on_top = False
    page.window.width = 800  # Ancho adecuado para todos los elementos
    page.window.height = 680  # Altura levemente menor para asegurar visibilidad de la barra de título
    page.window.center()  # Centrar la ventana en la pantalla
    
    # Configurar la barra superior (solo maximizar/restaurar)
    page.appbar = create_appbar(page, save_window_preference)
    page.title = "Producción Papelera Entre Ríos"
    page.padding = 5  # Minimizar el padding para aprovechar mejor el espacio
    page.scroll = "auto"  # Habilitar scroll automático si es necesario
    page.tight = True  # Establecer el modo ajustado para reducir espacios innecesarios
    
    
    
    # Estado de la aplicación
    state = {"calidad": None, "turno": None}

    # Conexión a la base de datos
    db_path = os.path.join(APP_DIR, "produccion.db")
    db_conn = create_connection(db_path)
    create_table(db_conn)

    # Definición de rutas
    def route_change(route):
        page.views.clear()
        if page.route == "/":            
            page.views.append(producto_turno_view(page, state))            
        elif page.route == "/etiqueta":
            page.views.append(etiqueta_view(page, state, db_conn))  # Pasar la conexión aquí        
        page.update()            
        

    # Configurar el manejador de cambio de ruta
    page.on_route_change = route_change       
    
    page.go(page.route)  # Navegar a la ruta inicial

    

# Iniciar la aplicación
ft.app(target=main)