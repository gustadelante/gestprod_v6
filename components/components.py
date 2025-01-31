import flet as ft

def create_textbox(label, value="", read_only=False):
    """Crear un TextBox con una etiqueta."""
    return ft.TextField(
        label=label,
        value=value,
        read_only=read_only,
        border_color=ft.colors.BLUE_500,
        width=200,
    )

def create_dropdown(label, options, on_change=None):
    """Crear un Dropdown con una etiqueta y opciones."""
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(option) for option in options],
        on_change=on_change,
        width=200,
    )

def create_button(text, on_click=None):
    """Crear un botón con texto y una acción."""
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
    )