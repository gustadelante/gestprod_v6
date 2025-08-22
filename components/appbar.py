import flet as ft

def create_appbar(page, save_window_preference):
    """Crear una AppBar con botón para maximizar/restaurar ventana (sin cambio de tema)."""
    # Botón para maximizar/restaurar
    is_max = bool(getattr(page.window, "maximized", False))
    window_btn = ft.IconButton(
        icon=ft.icons.FULLSCREEN_EXIT if is_max else ft.icons.FULLSCREEN,
        tooltip="Restaurar" if is_max else "Maximizar",
    )

    def toggle_window(e):
        current = bool(getattr(page.window, "maximized", False))
        new_state = not current
        page.window.maximized = new_state
        # Actualizar botón
        window_btn.icon = ft.icons.FULLSCREEN_EXIT if new_state else ft.icons.FULLSCREEN
        window_btn.tooltip = "Restaurar" if new_state else "Maximizar"
        # Persistir preferencia
        try:
            save_window_preference("maximized" if new_state else "normal")
        except Exception:
            pass
        page.update()

    window_btn.on_click = toggle_window

    return ft.AppBar(
        title=ft.Text("Producción Papelera Entre Ríos", size=18),  # Título de la AppBar con tamaño reducido
        center_title=True,  # Centrar el título
        bgcolor=ft.colors.BLUE_500,  # Color de fondo de la AppBar
        toolbar_height=45,  # Reducir la altura de la barra de herramientas
        actions=[
            window_btn,
        ],
    )




"""
from flet import AppBar, IconButton, icons, Text, colors

class MyAppBar(AppBar):
    def __init__(self, switch_theme):
        super().__init__(
            title=Text("Producción Papelera Entre Rios"),
            actions=[IconButton(icon=icons.WB_SUNNY, on_click=switch_theme)]
        )

        return AppBar(
            title=Text("Producción Papelera Entre Ríos"),  # Título de la AppBar
            center_title=True,  # Centrar el título
            bgcolor=colors.BLUE_500,  # Color de fondo de la AppBar
            actions=[
                IconButton(
                    icon=icons.SUNNY,  # Icono del botón
                    on_click=switch_theme,  # Acción al hacer clic
                    tooltip="Cambiar tema",  # Texto emergente
                ),
            ],
        ) 
"""


""" import flet as ft

def create_appbar(page):
    
    def toggle_theme(e):
        # Cambiar entre modo claro y oscuro
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT        
        page.update()
        # Guardar la preferencia en el almacenamiento local
        page.client_storage.set("theme_mode", page.theme_mode.value)

    return ft.AppBar(
        title=ft.Text("Producción Papelera Entre Ríos"),  # Título de la AppBar
        center_title=True,  # Centrar el título
        bgcolor=ft.colors.BLUE_500,  # Color de fondo de la AppBar
        actions=[
            ft.IconButton(
                icon=ft.icons.SUNNY,  # Icono del botón
                on_click=toggle_theme,  # Acción al hacer clic
                tooltip="Cambiar tema",  # Texto emergente
            ),
        ],
    ) """