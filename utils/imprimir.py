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
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Registrar fuentes con trazo más ancho (si existen)
    try:
        # Intentar registrar Impact que tiene un trazo muy grueso
        pdfmetrics.registerFont(TTFont('Impact', 'impact.ttf'))
        fuente_gruesa = 'Impact'
    except Exception:
        try:
            # Intentar registrar Arial Black que tiene un trazo más grueso
            pdfmetrics.registerFont(TTFont('ArialBlack', 'arialbd.ttf'))
            fuente_gruesa = 'ArialBlack'
        except Exception:
            # Si no se puede registrar, usar Helvetica-Bold
            fuente_gruesa = 'Helvetica-Bold'
    
    # Función para dibujar texto con trazo extra grueso y espaciado entre caracteres
    def draw_bold_text(canvas, x, y, text, font_name, font_size, offset=0.5, char_spacing=1.5):
        """Dibuja texto con un trazo extra grueso mediante múltiples impresiones y espaciado entre caracteres."""
        # Guardar estado actual
        canvas.saveState()
        canvas.setFont(font_name, font_size)
        
        # Calcular ancho de cada carácter para el espaciado
        char_widths = [canvas.stringWidth(char, font_name, font_size) for char in text]
        
        # Función para dibujar el texto completo con espaciado
        def draw_spaced_text(x_pos, y_pos):
            current_x = x_pos
            for i, char in enumerate(text):
                canvas.drawString(current_x, y_pos, char)
                current_x += char_widths[i] * char_spacing  # Aplicar espaciado entre caracteres
        
        # Dibujar el texto varias veces con pequeños desplazamientos para simular trazo más grueso
        draw_spaced_text(x-offset, y)
        draw_spaced_text(x+offset, y)
        draw_spaced_text(x, y-offset)
        draw_spaced_text(x, y+offset)
        draw_spaced_text(x, y)  # Texto central
        
        # Restaurar estado
        canvas.restoreState()
    
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
        y = height - 281 + 28.35  # Coordenada Y inicial (subida 1 cm = 28.35 points)
        line_height = 110  # Altura de cada línea
        x_left = 72  # Coordenada X para la primera columna
        x_right = 300 + 28.35  # Coordenada X para la segunda columna (1 cm = 28.35 points)
        
        # Primera fila: ancho y diámetro (bajada 0.5 cm = 14.175 points)
        # Usar técnica de trazo extra grueso
        c.setFont("Helvetica", 57)
        c.drawString(x_left - 28.35, y - 14.175 - 28.35 + 14.175 + 8.505, f"{nueva_bobina.ancho}")  # Trazo normal, bajado 0,2 cm
        # Línea eliminada - era una duplicación
        c.setFont("Helvetica", 57)
        c.drawString(x_right, y - 14.175 - 28.35 + 14.175 + 8.505, f"{nueva_bobina.diametro}")  # Trazo normal, bajado 0,2 cm
        
        # Segunda fila: gramaje y peso (posición original)
        y -= line_height
        # Usar técnica de trazo extra grueso
        c.setFont("Helvetica", 57)
        c.drawString(x_left - 28.35, y - 28.35 + 14.175, f"{nueva_bobina.gramaje}")  # Trazo normal, bajado 0,5 cm
        draw_bold_text(c, x_right, y - 28.35 + 14.175, f"{nueva_bobina.peso}", fuente_gruesa, 57, offset=0.5, char_spacing=1.25)  # Bajado 0,5 cm
        y -= line_height
        # Usar técnica de trazo extra grueso
        draw_bold_text(c, x_left - 28.35, y - 28.35 + 14.175, f"{nueva_bobina.bobina_nro}/{nueva_bobina.sec}", fuente_gruesa, 57, offset=0.5, char_spacing=1.25)  # Movido 1 cm a la izquierda, bajado 0,5 cm
        draw_bold_text(c, x_right, y - 28.35 + 14.175, f"{nueva_bobina.orden_fab}", fuente_gruesa, 57, offset=0.5, char_spacing=1.25)  # Bajado 0,5 cm
        y -= line_height
        # Subir 1 cm y bajar 0.5 cm la fila de fecha/turno
        c.setFont("Helvetica", 26)
        c.drawString(x_left, y + 28.35 - 14.175, f"{nueva_bobina.fecha}")
        # Usar técnica de trazo extra grueso para el turno
        c.setFont("Helvetica", 40)
        c.drawString(x_right, y + 28.35 - 14.175, f"{nueva_bobina.turno}")  # Trazo normal
        y -= line_height
        y -= line_height        
        c.setFont("Helvetica", 18)    
        c.drawString((x_left + 99.22 + 28.35), (y+3) + 28.35 + 28.35 - 14.175, f"{metros} Metros Lineales Aprox.")  # Bajado 0.5 cm (14.175 points)
        
        # Dibujar QR si existe (también subido 1 cm)
        if img_path and os.path.exists(img_path):
            c.drawImage(img_path, (x_left + 369.22), (y+72) + 28.35, width=144, height=144, mask='auto')
        
        c.showPage()
        c.save()
        
        # Enviar el archivo PDF directamente a la impresora en Windows
        try:
            # Asegurar que el archivo existe antes de intentar imprimirlo
            if os.path.exists(pdf_path):
                print(f"Enviando a imprimir: {pdf_path}")
                # Usar subprocess para mayor control y mejor manejo de errores
                import subprocess
                subprocess.run(["powershell", "Start-Process", "-FilePath", pdf_path, "-Verb", "Print"], 
                               check=True, capture_output=True)
                print("Comando de impresión enviado correctamente")
            else:
                print(f"Error: El archivo PDF no existe en la ruta: {pdf_path}")
                resultado["mensaje"] = f"Error: El archivo PDF no existe en la ruta: {pdf_path}"
                resultado["exito"] = False
        except Exception as e:
            print(f"Error al imprimir: {e}")
            resultado["mensaje"] = f"Advertencia: No se pudo imprimir. {str(e)}"
            resultado["exito"] = False
            
            # Intento alternativo con os.startfile si subprocess falla
            try:
                print("Intentando método alternativo de impresión...")
                os.startfile(pdf_path, "print")
                print("Método alternativo de impresión ejecutado")
            except Exception as e2:
                print(f"Error en método alternativo: {e2}")
        
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


