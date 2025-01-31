import flet as ft
from views.producto_turno import producto_turno_view
from views.etiqueta import etiqueta_view
from data.database import create_connection, create_table
from components.appbar import create_appbar  # Importar la AppBar
from utils.theme import switch_theme

# Ruta del archivo para guardar la preferencia del tema
THEME_PREFERENCE_FILE = "theme_preference.txt"

def load_theme_preference():
    """Cargar la preferencia del tema desde el archivo."""
    try:
        with open(THEME_PREFERENCE_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "light"  # Tema predeterminado si el archivo no existe

def save_theme_preference(theme_mode):
    """Guardar la preferencia del tema en el archivo."""
    with open(THEME_PREFERENCE_FILE, "w") as file:
        file.write(theme_mode)



def main(page: ft.Page):
       
    # Configuración de la página

    # Cargar la preferencia del tema al iniciar la aplicación
    theme_preference = load_theme_preference()
    page.theme_mode = ft.ThemeMode(theme_preference)  # Configurar el tema
    page.appbar = create_appbar(page, save_theme_preference)  # Pasar la función para guardar la preferencia  
    page.title = "Producción Papelera Entre Ríos"
    page.theme_mode = ft.ThemeMode.LIGHT  # Modo claro por defecto
    page.padding = 20
    
    
    
    # Estado de la aplicación
    state = {"calidad": None, "turno": None}

    # Conexión a la base de datos
    db_conn = create_connection("produccion.db")
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