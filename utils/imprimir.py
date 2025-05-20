import flet as ft
import openpyxl
import os
from data.database import init_db, insert_bobina, update_bobina, bobina_exists, get_max_sec
import qrcode
from PIL import Image

def calcular_metros(peso, gramaje, ancho):
    try:
        peso = float(peso)
        gramaje = float(gramaje)
        ancho = float(ancho)
        metros = (100000 * peso) / (gramaje * ancho)
        return round(metros)
    except ValueError as e:
        print(f"Error al calcular metros: {e}")
        return None

def genera_qr(bobina):
    try:

        qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(bobina)
        qr.make(fit=True)
        img = qr.make_image()                
        img.save("qr.png") 

    except:
        print(f"Error al generar QR")
        return None


def imprimir_y_guardar(db_conn, nueva_bobina):
    init_db()
    
    # Enviar los datos a la impresora
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas


    #calcula los metros
    metros = calcular_metros(nueva_bobina.peso, nueva_bobina.gramaje, nueva_bobina.ancho)
    if metros is not None:
        print(f"Metros: {metros}")

    
    c = canvas.Canvas("print_output.pdf", pagesize=A4)
    width, height = A4

    #genera QR
    genera_qr(f"{nueva_bobina.bobina_nro}/{nueva_bobina.sec}-{nueva_bobina.peso}")
    #aplica el QR en coordenadas
    img_path = "qr.png"
    if os.path.exists(img_path):
        image = Image.open(img_path)
        #x_pos = x_right -200 #pos horizontal
        #y_pos = y - 100 #pos vertical
        #image.x = 100
        #image.y = 100
        #c.insert_image(image)
        #c.drawImage(img_path,480,140,width=90,height=90,mask='auto')
        


    # Definir las coordenadas y el tamaño de la letra
    y = height - 281  # Coordenada Y inicial
    line_height = 110  # Altura de cada línea
    x_left = 72  # Coordenada X para la primera columna
    x_right = 300 + 28.35  # Coordenada X para la segunda columna (1 cm = 28.35 points)

    c.setFont("Helvetica-Bold", 45)
    c.drawString(x_left, y, f"{nueva_bobina.ancho}")
    c.drawString(x_right, y, f"{nueva_bobina.diametro}")
    y -= line_height
    c.drawString(x_left, y, f"{nueva_bobina.gramaje}")
    c.drawString(x_right, y, f"{nueva_bobina.peso}")
    y -= line_height
    c.drawString(x_left, y, f"{nueva_bobina.bobina_nro}/{nueva_bobina.sec}")
    c.drawString(x_right, y, f"{nueva_bobina.orden_fab}")
    y -= line_height
    c.setFont("Helvetica", 26)
    c.drawString(x_left, y, f"{nueva_bobina.fecha}")
    c.setFont("Helvetica-Bold", 40)
    c.drawString(x_right, y, f"{nueva_bobina.turno}")
    y -= line_height
    y -= line_height        
    c.setFont("Helvetica", 18)    
    c.drawString((x_left + 99.22), (y+3), f"{metros} Metros Lineales Aprox.")
    c.drawImage(img_path,(x_left + 369.22), (y+72),width=144,height=144,mask='auto')

    #c.drawString((x_left + 150.22), (y+3),  f"{metros} Metros Lineales Aprox.")

    #Metros 
    #txt_metros.Text = Convert.ToString((100000 * Convert.ToInt32(txt_peso.Text) / ((Convert.ToInt32(txt_gramaje.Text) * (Convert.ToDecimal(txt_ancho.Text, new CultureInfo("es-ES")))))));
    #txt_metros.Text = 
    # ((100000 * Convert.ToInt32(txt_peso.Text) / ((Convert.ToInt32(txt_gramaje.Text) * (Convert.ToDecimal(txt_ancho.Text, new CultureInfo("es-ES")))))));

    c.showPage()
    c.save()

    # Enviar el archivo PDF directamente a la impresora en Windows
    #os.system(f'start /min "" "print_output.pdf" /p') # Abre el pdf y lo deja en pantalla   
    os.startfile("print_output.pdf", "print")  
    
    

    # Guardar los valores en un archivo Excel
    file_path = "nueva_bobina.xlsx"
    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # Agregar encabezados si es un nuevo archivo
        sheet.append([
            "Ancho", "Diámetro", "Gramaje", "Peso", "Bobina Nro", "Sec", 
            "Orden de Fabricación", "Fecha", "Turno", "CodProd", "DescProd"
        ])

    sheet.append([
        nueva_bobina.ancho,
        nueva_bobina.diametro,
        nueva_bobina.gramaje,
        nueva_bobina.peso,
        nueva_bobina.bobina_nro,
        nueva_bobina.sec,
        nueva_bobina.orden_fab,
        nueva_bobina.fecha,
        nueva_bobina.turno,
        nueva_bobina.calidad[:2],  # codprod
        nueva_bobina.calidad[3:],  # descprod
    ])
    workbook.save(file_path)

    # Check if bobina exists in the database and insert or update accordingly
    if bobina_exists(db_conn, nueva_bobina):
        res = update_bobina(db_conn, nueva_bobina)        
    else:
        res = insert_bobina(db_conn, nueva_bobina)        
    

    try:
        # Lógica para imprimir y guardar
        # ...
        resultado = {            
            "datos_bobina_dict": {
                "mensaje": res["mensaje"],
                "nro_of": res["nro_of"],
                "bobina_nro": res["nro_bobina"],
                "bobina_izq": res["bobina_izq"],
                "peso_bobina": res["peso_bobina"],
                # Otros datos de la bobina
            }
        }
    except Exception as e:
        print(f"Error al imprimir y guardar: {e}")
        resultado = {
            "mensaje": "Error al imprimir y guardar",
            "datos_bobina_dict": {
                "bobina_nro": nueva_bobina.bobina_nro,
                # Otros datos de la bobina
            }
        }

    return resultado    
    #return nueva_bobina.bobina_nro, resultado


   # return nueva_bobina.bobina_nro, res


