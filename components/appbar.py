import flet as ft

def create_appbar(page, save_theme_preference):
    """Crear una AppBar con un botón para cambiar entre modo claro y oscuro."""
    def toggle_theme(e):
        # Cambiar entre modo claro y oscuro
        new_theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.theme_mode = new_theme_mode
        page.update()

        # Guardar la preferencia del usuario
        save_theme_preference(new_theme_mode.value)

    return ft.AppBar(
        title=ft.Text("Producción Papelera Entre Ríos"),  # Título de la AppBar
        center_title=True,  # Centrar el título
        bgcolor=ft.colors.BLUE_500,  # Color de fondo de la AppBar
        toolbar_height=60,
        actions=[
            ft.IconButton(
                icon=ft.icons.SUNNY,  # Icono del botón
                on_click=toggle_theme,  # Acción al hacer clic
                tooltip="Cambiar tema",  # Texto emergente                
            ),
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