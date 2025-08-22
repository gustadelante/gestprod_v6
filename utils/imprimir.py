import flet as ft
import openpyxl
import os
import sys
import tempfile
from data.database import init_db, insert_bobina, update_bobina, bobina_exists, get_max_sec
import qrcode
from PIL import Image

def get_app_dir() -> str:
    """Devuelve la carpeta donde está el ejecutable (.exe) o, en desarrollo, la carpeta del archivo actual."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # PyInstaller o flet pack (congelado)
        return os.path.dirname(sys.executable)
    # Desarrollo: usar la carpeta del archivo main.py
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subir un nivel desde utils

def get_writable_path(filename):
    """Intenta obtener una ruta donde se pueda escribir el archivo.
    Primero intenta en la carpeta del ejecutable, si no es posible, usa temp."""
    app_dir = get_app_dir()
    app_path = os.path.join(app_dir, filename)
    
    # Verificar si podemos escribir en la carpeta de la aplicación
    try:
        # Probar si podemos escribir en la carpeta
        test_path = os.path.join(app_dir, "test_write_permission.tmp")
        with open(test_path, 'w') as f:
            f.write("test")
        os.remove(test_path)
        return app_path
    except (IOError, PermissionError):
        # Si no podemos escribir, usar carpeta temporal
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, filename)

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
        qr_path = get_writable_path("qr.png")
        img.save(qr_path)
        return qr_path
    except Exception as e:
        print(f"Error al generar QR: {e}")
        return None


def imprimir_y_guardar(db_conn, nueva_bobina):
    init_db()
    resultado = {"mensaje": "Operación completada", "exito": True}
    
    # Enviar los datos a la impresora
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    
    #calcula los metros
    metros = calcular_metros(nueva_bobina.peso, nueva_bobina.gramaje, nueva_bobina.ancho)
    if metros is not None:
        print(f"Metros: {metros}")
    
    try:
        # Obtener rutas donde podemos escribir
        pdf_path = get_writable_path("print_output.pdf")
        excel_path = get_writable_path("nueva_bobina.xlsx")
        
        # Crear PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # Generar QR
        qr_data = f"{nueva_bobina.bobina_nro}/{nueva_bobina.sec}-{nueva_bobina.peso}"
        img_path = genera_qr(qr_data)
        
        if not img_path or not os.path.exists(img_path):
            resultado["mensaje"] = "Advertencia: No se pudo generar el código QR"
            resultado["exito"] = False
            img_path = None
        
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
        
        # Dibujar QR si existe
        if img_path and os.path.exists(img_path):
            c.drawImage(img_path, (x_left + 369.22), (y+72), width=144, height=144, mask='auto')
        
        c.showPage()
        c.save()
        
        # Enviar el archivo PDF directamente a la impresora en Windows
        try:
            os.startfile(pdf_path, "print")
        except Exception as e:
            print(f"Error al imprimir: {e}")
            resultado["mensaje"] = f"Advertencia: No se pudo imprimir. {str(e)}"
            resultado["exito"] = False
        
        # Guardar los valores en un archivo Excel
        try:
            if os.path.exists(excel_path):
                workbook = openpyxl.load_workbook(excel_path)
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
            workbook.save(excel_path)
            
            # Informar al usuario dónde se guardó el archivo
            resultado["excel_path"] = excel_path
            print(f"Excel guardado en: {excel_path}")
        except Exception as e:
            print(f"Error al guardar Excel: {e}")
            resultado["mensaje"] = f"Advertencia: No se pudo guardar el archivo Excel. {str(e)}"
            resultado["exito"] = False
    except Exception as e:
        print(f"Error general: {e}")
        resultado["mensaje"] = f"Error: {str(e)}"
        resultado["exito"] = False

    # Check if bobina exists in the database and insert or update accordingly
    if bobina_exists(db_conn, nueva_bobina):
        res = update_bobina(db_conn, nueva_bobina)        
    else:
        res = insert_bobina(db_conn, nueva_bobina)        

    # Agregar datos de la base de datos al resultado
    resultado["datos_bobina_dict"] = {
        "mensaje": res.get("mensaje", "Operación completada"),
        "nro_of": res.get("nro_of", ""),
        "bobina_nro": res.get("nro_bobina", nueva_bobina.bobina_nro),
        "bobina_izq": res.get("bobina_izq", ""),
        "peso_bobina": res.get("peso_bobina", nueva_bobina.peso),
        }

    return resultado    
    #return nueva_bobina.bobina_nro, resultado


   # return nueva_bobina.bobina_nro, res


