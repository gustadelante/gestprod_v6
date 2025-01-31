import flet as ft
from components import create_textbox, create_button

def etiqueta_view(page, state, db_conn):





    """Vista para ingresar datos de producción."""
    def save_data(e):
        if all([ancho.value, diametro.value, gramaje.value, peso.value, bobina_num.value, of.value, fecha.value]):
            data = (
                state["calidad"],
                state["turno"],
                ancho.value,
                diametro.value,
                gramaje.value,
                peso.value,
                bobina_num.value,
                of.value,
                fecha.value,
            )
            from data.database import insert_data  # Importar aquí para evitar dependencias circulares
            insert_data(db_conn, data)
            page.snack_bar = ft.SnackBar(content=ft.Text("Datos guardados correctamente."))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Complete todos los campos."))
            page.snack_bar.open = True
        page.update()

    calidad_textbox = create_textbox(
        label="Calidad",
        value=state["calidad"],
        read_only=True,
    )

    turno_textbox = create_textbox(
        label="Turno",
        value=state["turno"],
        read_only=True,
    )

    ancho = create_textbox(label="ANCHO")
    diametro = create_textbox(label="DIAMETRO")
    gramaje = create_textbox(label="GRAMAJE")
    peso = create_textbox(label="PESO")
    bobina_num = create_textbox(label="BOBINA Nº")
    of = create_textbox(label="OF")
    fecha = create_textbox(label="FECHA")

    imprimir_button = create_button(
        text="Imprimir",
        on_click=save_data,
    )

    return ft.View(
        "/etiqueta",
        controls=[
            ft.Row(
                controls=[                                        
                    ft.Text("IMPRESIÓN DE ETIQUETAS",text_align=ft.TextAlign.CENTER, size=40, weight=ft.FontWeight.W_500, color=ft.colors.GREEN_900),
                ]
            ),
            ft.Column(
                controls=[
                    calidad_textbox,
                    turno_textbox,
                    ancho,
                    diametro,
                    gramaje,
                    peso,
                    bobina_num,
                    of,
                    fecha,
                    imprimir_button,
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )