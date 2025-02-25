import flet as ft
from components import create_dropdown, create_button
from components.appbar import create_appbar  # Importar la AppBar
from utils.theme import switch_theme

def producto_turno_view(page, state):
    # Establecer el tamaño y posición de la ventana
    page.window.width = 700
    page.window.height = 800
    page.window.center()  # centra la ventana en la pantalla
    page.window.resizable = True        
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "light"
    page.bgcolor = ft.colors.BLUE_GREY_800    
    page.autoscroll = True
    #page.scroll = True
    #page.expand = True        
    page.update()
    print(page.horizontal_alignment, page.vertical_alignment)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    print(page.horizontal_alignment, page.vertical_alignment)

    """Vista para seleccionar calidad y turno."""
    def validate_and_navigate(e):
        is_valid = True
        if not calidad_dropdown.value:
            calidad_dropdown.error_text = "Por favor, seleccione una calidad."
            calidad_dropdown.update()
            is_valid = False
        if not turno_dropdown.value:
            turno_dropdown.error_text = "Por favor, seleccione un turno."
            turno_dropdown.update()
            is_valid = False
        if is_valid:
            try:
                page.go("/etiqueta")  
            except:
                page.snack_bar = ft.SnackBar(content=ft.Text("Seleccione calidad y turno."))
                page.snack_bar.open = True

    def clear_error_text(e):
        if calidad_dropdown.error_text:
           calidad_dropdown.error_text = ""
           calidad_dropdown.update() 
        if turno_dropdown.error_text:
           turno_dropdown.error_text = "" 
           turno_dropdown.update()

    calidad_dropdown = create_dropdown(
        label="Calidad",
        options=["01-ONDA LINER", "02-COVERING", "03-L.BLANCO", "04-CART.GRIS", "05-CART.BLANCA", "06-LINER PER", "07-ONDA C", "08-ONDA EFL"],
        on_change=lambda e: state.update({"calidad": e.control.value}),
    )

    turno_dropdown = create_dropdown(
        label="Turno",
        options=["A", "B", "C", "D"],
        on_change=lambda e: state.update({"turno": e.control.value}),
    )

    ingresar_button = create_button(
        text="Ingresar",
        on_click=validate_and_navigate,
    )

    titulo = ft.Text(
        "Seleccione Calidad / Turno",
        color=ft.colors.GREEN_900,
        size=24,
        weight="bold",
        text_align=ft.TextAlign.CENTER
    )

    return ft.View(
        "/",
        controls=[            
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            titulo,
                                            ft.Divider(height=9, thickness=3, color="green"),
                                            calidad_dropdown,
                                            turno_dropdown,
                                            ingresar_button,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=20,
                                    alignment=ft.alignment.center,
                                    width=400  # Ajustar el ancho del Container
                                ),
                                elevation=2,
                                width=400  # Ajustar el ancho del Card
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
    )

