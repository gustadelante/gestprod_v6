import flet as ft
from components.components import create_textbox, create_button
from datetime import datetime
from utils.imprimir import imprimir_y_guardar
from data.producto import bobina

def etiqueta_view(page, state, db_conn):

     # Ajuste del tamaño de la ventana
    page.window_width = 800 #900
    page.window_height = 750 #800

    # Colores para modo claro y oscuro con verde oscuro predominante
    light_primary_color = ft.colors.GREEN
    dark_primary_color = ft.colors.GREEN_900
    light_background_color = ft.colors.WHITE
    dark_background_color = ft.colors.BLACK
    light_text_color = ft.colors.BLACK
    dark_text_color = ft.colors.WHITE


    #saco el mensaje de no completado de drpodowns
    # Limpiar el error de no completado
    def clear_error_text(e):
        if calidad.error_text:
           calidad.error_text = ""
           calidad.update() 
        if turno.error_text:
           turno.error_text = "" 
           turno.update()

    # Validar contenido de los text field
    def validate_float(e):
        if not e.control.value.replace(",", "", 1).isdigit() or len(e.control.value) > 5:
            e.control.error_text = "Número no válido o demasiado largo"
        else:
            e.control.error_text = ""
        page.update()

    def validate_int(e):
        if not e.control.value.isdigit() or len(e.control.value) > 5:
            e.control.error_text = "Número no válido o demasiado largo"
        else:
            e.control.error_text = ""
        page.update()

    def validate_single_digit(e):
        if not e.control.value.isdigit() or len(e.control.value) != 1:
            e.control.error_text = "Debe ser un solo dígito"
        else:
            e.control.error_text = ""
        page.update()

    #Templates
    def create_text_field(label, on_change, mode):
        fill_color = dark_background_color if mode == "dark" else ft.colors.GREY_200
        text_color = dark_text_color if mode == "dark" else light_text_color
        return ft.TextField(
            label=label, on_change=on_change,
            text_size=26, width=400,
            border_radius=10, filled=True, fill_color=fill_color,
            color=text_color,
            border_color=ft.Colors.RED_800, 
            border_width=10,
            hover_color=ft.colors.GREEN_100
        )    

    def create_dropdown(label, options, mode):
        fill_color = dark_background_color if mode == "dark" else ft.colors.GREY_200
        text_color = dark_text_color if mode == "dark" else light_text_color        
        return ft.Dropdown(
            label=label, options=options,
            text_size=20, width=400,
            border_radius=10, filled=True, fill_color=fill_color,
            color=text_color,
            border_color=ft.Colors.RED_800, 
            border_width=10,
            on_change=clear_error_text
        )
    

#Definir los campos de la vista
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

    ancho = create_text_field("ANCHO", validate_float, page.theme_mode)    
    diametro = create_text_field("DIÁMETRO", validate_int, page.theme_mode)
    gramaje = create_text_field("GRAMAJE", validate_int, page.theme_mode)
    peso = create_text_field("PESO", validate_float, page.theme_mode)
    bobina_num = create_text_field("BOBINA Nº", validate_int, page.theme_mode)
    sec = create_text_field("SEC", validate_single_digit, page.theme_mode)
    orden_fab = create_text_field("ORDEN FAB", validate_int, page.theme_mode)
    now = datetime.now()
    fecha_str = now.strftime("%Y-%m-%d %H:%M")

    fecha_container = create_text_field("Fecha y Hora", lambda e: None, page.theme_mode)
    fecha_container.value = fecha_str

    #Definir opciones de los dropdowns
    turno_options = [ft.dropdown.Option("A"), ft.dropdown.Option("B"), ft.dropdown.Option("C"), ft.dropdown.Option("D")]
    calidad_options = [ft.dropdown.Option("01-ONDA LINER"), ft.dropdown.Option("02-COVERING"), ft.dropdown.Option("03-L.BLANCO")
                       , ft.dropdown.Option("04-CART.GRIS"), ft.dropdown.Option("05-CART.BLANCA"), ft.dropdown.Option("06-LINER PER")
                       , ft.dropdown.Option("07-ONDA C"), ft.dropdown.Option("08-ONDA EFL")
    ]

    turno = create_dropdown("Turno", turno_options, page.theme_mode)
    calidad = create_dropdown("Calidad", calidad_options, page.theme_mode)

    turno.value = state["turno"]
    calidad.value = state["calidad"]
    sec.value = 1


    def set_sec_value(sec, bobina_nro):
        from data.database import get_max_sec  # Importar aquí para evitar dependencias circulares
        try:
            max_sec = get_max_sec(bobina_nro)
            nuevo_sec = max_sec + 1
            sec.value = str(nuevo_sec)
            print(f"nuevo sec: {sec.value}")
        except Exception as e:
            print("No pudo incrementar el valor de la secuencia:", e)
            sec.value = "1"
        sec.update()


    def verificar_datos():
        campos = [ancho, diametro, gramaje, peso, bobina_num, sec, orden_fab, turno, calidad]
        for campo in campos:
            if campo.value == "":
                return campo
            if campo.label == "Turno" and campo.value == None:
                return campo 
            if campo.label == "Calidad" and campo.value == None:
                return campo
        return None
    
    def cerrar_dialogo_y_enfocar(e, dialog, campo):
        dialog.open = False
        campo.focus()
        page.update()

    def handle_imprimir_y_guardar(nueva_bobina, sec):
        bobina_nro = imprimir_y_guardar(db_conn, nueva_bobina)
        set_sec_value(sec, bobina_nro)

    def imprimir_datos(e):
        old_sec = sec.value
        campo_incompleto = verificar_datos()
        if campo_incompleto:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Debe completar todos los campos"),
                actions=[
                    ft.TextButton(
                        text="Aceptar",
                        on_click=lambda e: cerrar_dialogo_y_enfocar(e, dialog, campo_incompleto)
                    )
                ]
            )
            page.dialog = dialog
            dialog.open = True
        else:
            datos = {
                "ANCHO": ancho.value,
                "DIÁMETRO": diametro.value,
                "GRAMAJE": gramaje.value,
                "PESO": peso.value,
                "Bobina Nro": bobina_num.value,
                "Sec": sec.value,
                "Orden de Fabricación": orden_fab.value,
                "Fecha y Hora": fecha_str,
                "Turno": turno.value,
                "Calidad": calidad.value
            }
            params = {
                ancho.value,
                diametro.value,
                gramaje.value,
                peso.value,
                bobina_num.value,
                sec.value,
                orden_fab.value,
                fecha_str,
                turno.value,
                calidad.value
            }            
            print(datos)
            # Llamada a la función con los campos ingresados
            funcion_procesar_datos(datos)
            # llamada a metodo de producto.py
            nueva_bobina = bobina(ancho.value,
                diametro.value,
                gramaje.value,
                peso.value,
                bobina_num.value,
                sec.value,
                orden_fab.value,
                fecha_str,
                turno.value,
                calidad.value)
            # Llamada a la función para imprimir y guardar
            handle_imprimir_y_guardar(nueva_bobina, sec)

        page.update()    

    # Definición de la función para procesar los datos
    def funcion_procesar_datos(datos):
        # Implementación de lógica
        pass


    imprimir_button = ft.ElevatedButton(
        text="IMPRIMIR",
        on_click=imprimir_datos,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 20, 20, 20),
            text_style=ft.TextStyle(size=22, weight="bold"),
            #bgcolor=page.theme.primary_color, 
            bgcolor=ft.colors.BLUE_GREY_100,
            color=ft.colors.GREEN_900,
        )
    )

    responsive_grid = ft.GridView(
        expand=True,
        max_extent=400,
        #padding=10,
        child_aspect_ratio=3.6,        
        controls=[            
            ft.Container(content=ancho, alignment=ft.alignment.center),
            ft.Container(content=diametro, alignment=ft.alignment.center),
            ft.Container(content=gramaje, alignment=ft.alignment.center),
            ft.Container(content=peso, alignment=ft.alignment.center),
            ft.Container(content=ft.Row(
                [
                    ft.Container(content=bobina_num, alignment=ft.alignment.center, expand=7),
                    ft.Container(content=sec, alignment=ft.alignment.center, expand=3)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
            alignment=ft.alignment.center),
            ft.Container(content=orden_fab, alignment=ft.alignment.center),
            ft.Container(content=fecha_container, alignment=ft.alignment.center),
            ft.Container(content=turno, alignment=ft.alignment.center),
            ft.Container(content=calidad, alignment=ft.alignment.center),
            ft.Container(content=imprimir_button, alignment=ft.alignment.center)
        ],
    )

    titulo = ft.Row(
        controls=[
            ft.Text(
                value="IMPRESION DE ETIQUETAS",
                text_align=ft.TextAlign.CENTER,
                size=40,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREEN_900
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.View(
            controls=[
                titulo,
                ft.Divider(height=9, thickness=3, color="green"),
                ft.Card(
                    ft.Container(
                        content=ft.Column([
                            responsive_grid
                        ]),
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.colors.GREEN_300,
                        alignment=ft.alignment.center,
                    )

                ),
                                
            ]

    )

"""
    
    Vista para ingresar datos de producción.

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

    

    #of = create_textbox(label="OF")
    #fecha = create_textbox(label="FECHA")

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

    """