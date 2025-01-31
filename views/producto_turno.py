import flet as ft
from components import create_dropdown, create_button
from components.appbar import create_appbar  # Importar la AppBar
from utils.theme import switch_theme



def producto_turno_view(page, state):
        
    #print("New page size:", page.window.width, page.window.height)
    # Establecer el tamaño y posición de la ventana
    page.window.width = 750    
    page.window.height = 800    
    page.window.center()  # Esto centrará la ventana en la pantalla    
    page.window.resizable = True 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = True        
    page.update()

   
    #print("New page size:", page.window.width, page.window.height)

        

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
        
        """
        if not state["calidad"] or not state["turno"]:
            page.snack_bar = ft.SnackBar(content=ft.Text("Seleccione calidad y turno."))
            page.snack_bar.open = True
            #page.update()
        else:
            page.go("/etiqueta")
        """       
    # Limpiar el error de no completado
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

    return ft.View(
        "/",        
        controls=[            
            ft.Column(
                controls=[                    
                    calidad_dropdown,
                    turno_dropdown,
                    ingresar_button,                    
                ],
                expand=True,
                #margin=ft.margin.only(top=60),  # Margen superior = altura de la AppBar
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.MainAxisAlignment,
            )            
        ],
    )