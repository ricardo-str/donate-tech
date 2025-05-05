import pymysql
import json


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

# Carga el archivo .json que contiene las consultas
with open('database/sentencias.json', 'r') as querys:
    QUERY_DICT = json.load(querys)

def get_conn():
    conn = pymysql.connect(
        db=DB_NAME,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        charset=DB_CHARSET
    )
    return conn

def get_db():
    conn = get_conn()
    return conn, conn.cursor()

def create_contacto(nombre, email, celular, comuna, region):
    conn, cursor = get_db()
    
    # Obtener region_id
    cursor.execute("SELECT id FROM region WHERE nombre = %s", (region,))
    region_result = cursor.fetchone()
    if not region_result:
        raise ValueError(f"Región no encontrada: {region}")
    region_id = region_result[0]
    
    # Obtener comuna_id
    cursor.execute("SELECT id FROM comuna WHERE nombre = %s AND region_id = %s", (comuna, region_id))
    comuna_result = cursor.fetchone()
    if not comuna_result:
        raise ValueError(f"Comuna no encontrada: {comuna} en la región {region}")
    comuna_id = comuna_result[0]
    
    cursor.execute(QUERY_DICT["insert_contacto"], (nombre, email, celular, comuna_id))
    conn.commit()
    contacto_id = cursor.lastrowid
    conn.close()
    return contacto_id

def create_dispositivo(contacto_id, nombre, descripcion, tipo, anos_uso, estado, fotos):
    print(f"Ejecutando create_dispositivo con: {contacto_id}, {nombre}, {descripcion}, {tipo}, {anos_uso}, {estado}, {fotos}")
    conn, cursor = get_db()
    try:
        print(f"Ejecutando consulta: {QUERY_DICT['insert_dispositivo']}")
        cursor.execute(QUERY_DICT["insert_dispositivo"], (contacto_id, nombre, descripcion, tipo, anos_uso, estado))
        dispositivo_id = cursor.lastrowid
        print(f"Dispositivo creado con ID: {dispositivo_id}")
        
        for foto in fotos:
            print(f"Insertando foto: {foto}")
            cursor.execute(QUERY_DICT["insert_archivo"], (foto, foto, dispositivo_id))
        
        conn.commit()
        print("Commit realizado")
        return dispositivo_id
    except Exception as e:
        conn.rollback()
        print(f"Error en create_dispositivo: {e}")
        raise e
    finally:
        conn.close()

def get_dispositivos(page, per_page):
    conn, cursor = get_db()
    offset = (page - 1) * per_page
    try:
        cursor.execute(QUERY_DICT["get_dispositivos"], (per_page, offset))
        dispositivos = cursor.fetchall()
        
        # Convertir los resultados en diccionarios
        columns = [col[0] for col in cursor.description]
        dispositivos = [dict(zip(columns, row)) for row in dispositivos]
        
        cursor.execute(QUERY_DICT["count_dispositivos"])
        total = cursor.fetchone()[0]
        return dispositivos, total
    except Exception as e:
        print(f"Error en get_dispositivos: {e}")
        return [], 0
    finally:
        conn.close()
    

def get_contacto_by_id(id):
    conn, cursor = get_db()
    cursor.execute(QUERY_DICT["get_contacto_by_id"], (id,))
    contacto = cursor.fetchone()
    conn.close()
    return contacto

def get_dispositivos_by_contacto(contacto_id):
    conn, cursor = get_db()
    cursor.execute(QUERY_DICT["get_dispositivos_by_contacto"], (contacto_id,))
    dispositivos = cursor.fetchall()
    conn.close()
    return dispositivos

def get_dispositivo_by_id(id):
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["get_dispositivo_by_id"], (id,))
        dispositivo = cursor.fetchone()
        if dispositivo:
            columns = [col[0] for col in cursor.description]
            dispositivo = dict(zip(columns, dispositivo))
            
            cursor.execute(QUERY_DICT["get_fotos_by_dispositivo"], (id,))
            fotos = cursor.fetchall()
            dispositivo['fotos'] = [foto['nombre_archivo'] for foto in fotos]
        return dispositivo
    finally:
        conn.close()

def get_dispositivo_info(id):
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["get_dispositivo_info"], (id,))
        dispositivo = cursor.fetchone()
        if dispositivo:
            columns = [col[0] for col in cursor.description]
            dispositivo = dict(zip(columns, dispositivo))
            
            cursor.execute(QUERY_DICT["get_archivos_by_dispositivo"], (id,))
            fotos = cursor.fetchall()
            dispositivo['fotos'] = []
            for foto in fotos:
                foto_dict = dict(zip([column[0] for column in cursor.description], foto))
                dispositivo['fotos'].append({'ruta_archivo': foto_dict['nombre_archivo']})
        return dispositivo
    finally:
        conn.close()

def create_comentario(nombre, texto, dispositivo_id):
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["create_comentario"], (nombre, texto, dispositivo_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error al crear comentario: {e}")
        raise e
    finally:
        conn.close()

def get_comentarios_by_dispositivo(dispositivo_id):
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["get_comentarios_by_dispositivo"], (dispositivo_id,))
        comentarios = cursor.fetchall()
        # Devuelve los comentarios como una lista de diccionarios
        columns = [col[0] for col in cursor.description]
        comentarios = [dict(zip(columns, row)) for row in comentarios]
        return comentarios
    except Exception as e:
        print(f"Error al obtener comentarios: {e}")
        return []
    finally:
        conn.close()

def get_dispositivos_por_tipo():
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["get_dispositivos_por_tipo"])  
        dispositivos = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        dispositivos = [dict(zip(columns, row)) for row in dispositivos]
        return dispositivos
    except Exception as e:
        print(f"Error al obtener dispositivos por tipo: {e}")
        return []
    finally:
        conn.close()

def get_contactos_por_comuna():
    conn, cursor = get_db()
    try:
        cursor.execute(QUERY_DICT["get_contactos_por_comuna"])
        contactos = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in contactos]
    except Exception as e:
        print(f"Error al obtener contactos por comuna: {e}")
        return []
    finally:
        conn.close()


