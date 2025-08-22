import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Crear una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión exitosa a SQLite: {db_file}")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def init_db():
    """Inicializar la base de datos."""
    conn = create_connection("produccion.db")
    create_table(conn)
    conn.close()


def create_table(conn):
    """Crear la tabla para almacenar los datos de producción."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bobina (
                id INTEGER PRIMARY KEY AUTOINCREMENT,                
                turno TEXT NOT NULL,
                ancho REAL NOT NULL,
                diametro REAL NOT NULL,
                gramaje REAL NOT NULL,
                peso REAL NOT NULL,
                bobina_num TEXT NOT NULL,
                sec TEXT,                       
                of TEXT NOT NULL,
                fecha TEXT NOT NULL,
                codprod TEXT,
                descprod TEXT,
                tipo_mov TEXT DEFAULT 'ALTA',
                alistamiento TEXT DEFAULT '01',
                calidad TEXT,
                observaciones TEXT,
                obs TEXT,
                tipomovimiento TEXT DEFAULT '006',
                deposito TEXT DEFAULT '01',
                codigoDeProducto TEXT,
                primeraUnDeMedida TEXT DEFAULT 'KG',
                CantidadEnPrimeraUdM TEXT DEFAULT '00000000000001',
                lote TEXT,
                fechaValidezLote TEXT,
                fechaElaboracion TEXT,
                nroOT TEXT,
                codclie TEXT DEFAULT '000011',
                cuentacontable TEXT DEFAULT '1401010000',
                metros TEXT,
                producto TEXT,
                segundaUnDeMedida TEXT DEFAULT 'UN',
                CantidadEnSegunda TEXT DEFAULT '1',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP 
            )
        ''')
        conn.commit()
        print("Tabla 'bobina' creada o ya existente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insert_bobina(conn, nueva_bobina):
    """Insertar datos en la tabla 'bobina'."""

    db_conn = create_connection("produccion.db")
    try:
        cursor = db_conn.cursor()
        cursor.execute('''
             INSERT INTO bobina (ancho, diametro, gramaje, peso, bobina_num, sec, of, fecha, turno, codprod, descprod)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        nueva_bobina.ancho,
        nueva_bobina.diametro,
        nueva_bobina.gramaje,
        nueva_bobina.peso,
        nueva_bobina.bobina_nro,
        nueva_bobina.sec,
        nueva_bobina.orden_fab,
        nueva_bobina.fecha,
        nueva_bobina.turno,
        nueva_bobina.calidad[:2],  # codcal
        nueva_bobina.calidad[3:]   # descprod
        ))
        db_conn.commit()
        db_conn.close()
        print("Datos insertados correctamente.")        
        mensaje = "Datos insertados correctamente."
        nro_bobina_completo = str(nueva_bobina.bobina_nro) + str(nueva_bobina.sec)
        datos_bobina = (mensaje, str(nueva_bobina.orden_fab), str(nro_bobina_completo), str(nueva_bobina.bobina_nro), str(nueva_bobina.peso))
        if datos_bobina:
            # Crear diccionario con los datos de la bobina
            nombres_columnas = ["mensaje", "nro_of", "nro_bobina", "bobina_izq", "peso_bobina"]  # Nombre de las columnas
            datos_bobina_dict = dict(zip(nombres_columnas, datos_bobina))
        else:
            datos_bobina_dict = None


        #return mensaje, datos_bobina_dict
        return datos_bobina_dict
    except Error as e:
        print(f"Error al insertar datos: {e}")


def update_bobina(conn, nueva_bobina):
    #db_path = get_db_path()
    #conn = sqlite3.connect(db_path)
    try:
        db_conn = create_connection("produccion.db")
        cursor = db_conn.cursor()    
        cursor.execute('''
            UPDATE bobina
            SET ancho = ?, diametro = ?, gramaje = ?, peso = ?, of = ?, fecha = ?, turno = ?, codprod = ?, descprod = ?
            WHERE bobina_num = ? AND sec = ?
        ''', (
            nueva_bobina.ancho,
            nueva_bobina.diametro,
            nueva_bobina.gramaje,
            nueva_bobina.peso,
            nueva_bobina.orden_fab,
            nueva_bobina.fecha,
            nueva_bobina.turno,
            nueva_bobina.calidad[:2],  # codprod
            nueva_bobina.calidad[3:],  # descprod
            nueva_bobina.bobina_nro,
            nueva_bobina.sec
        ))
        db_conn.commit()
        db_conn.close()
        mensaje = "Datos actualizados correctamente."
        nro_bobina_completo = str(nueva_bobina.bobina_nro) + str(nueva_bobina.sec)
        datos_bobina = (mensaje, str(nueva_bobina.orden_fab), str(nro_bobina_completo), str(nueva_bobina.bobina_nro), str(nueva_bobina.peso))
        if datos_bobina:
            # Crear diccionario con los datos de la bobina
            nombres_columnas = ["mensaje", "nro_of", "nro_bobina", "bobina_izq", "peso_bobina"]  # Nombre de las columnas
            datos_bobina_dict = dict(zip(nombres_columnas, datos_bobina))
        else:
            datos_bobina_dict = None
        
        return datos_bobina_dict
    except Error as e:
        print(f"Error al insertar datos: {e}")

#def bobina_exists(nueva_bobina):
def bobina_exists(conn, nueva_bobina):    
    #db_path = get_db_path()
    #conn = sqlite3.connect(db_path)
    
    try:
        db_conn = create_connection("produccion.db")    
        cursor = db_conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM bobina WHERE bobina_num = ? AND sec = ?
        ''', (nueva_bobina.bobina_nro, nueva_bobina.sec))
        exists = cursor.fetchone()[0] > 0
        db_conn.close()
        return exists
    except Error as e:
        db_conn.close()
        print(f"Error al verificar si la bobina existe: {e}")
        return False

def get_max_sec(bobina_num):
    """Obtener el máximo valor de secuencia para una bobina."""
    try:
        db_conn = create_connection("produccion.db")    
        cursor = db_conn.cursor()
        cursor.execute('''
            SELECT MAX(CAST(sec AS INTEGER)) FROM bobina WHERE bobina_num = ?
        ''', (bobina_num,))
        max_sec = cursor.fetchone()[0]
        db_conn.close()
        return max_sec if max_sec is not None else 0        
    except Error as e:
        print(f"Error al obtener el máximo valor de secuencia: {e}")
        return 0       