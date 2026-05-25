# part1_backend y conexion con al database
import mysql.connector


def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="control_usuarios"
    )


def guardar_paciente_completo(cedula_id, p_datos, h_datos, c_datos, m_datos, s_datos):
    """
    Recibe la cédula manual como ID junto con las tuplas de datos desde el frontend.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        # 1. Datos Personales (Ahora insertamos la cédula manualmente en la columna id)
        sql_p = "INSERT INTO datos_personales (id, nombre, apellidos, telefono, correo) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_p, (cedula_id,) + p_datos)

        # 2. Historial Clínico (Usamos la cédula_id directamente)
        sql_h = "INSERT INTO historial_clinico (paciente_id, tipo_sangre, alergias, enfermedades_cronicas) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_h, (cedula_id,) + h_datos)

        # 3. Contactos Emergencia
        sql_c = "INSERT INTO contactos_emergencia (paciente_id, nombre_contacto, parentesco, telefono_emergencia) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_c, (cedula_id,) + c_datos)

        # 4. Consultas Médicas
        sql_m = "INSERT INTO consultas_medicas (paciente_id, fecha_consulta, motivo_consulta, diagnostico, medico_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_m, (cedula_id,) + m_datos)

        # 5. Signos Vitales
        sql_s = "INSERT INTO signos_vitales (paciente_id, fecha_registro, presion_arterial, frecuencia_cardiaca, temperatura) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_s, (cedula_id,) + s_datos)

        conexion.commit()
        return cedula_id
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()


def buscar_paciente_en_db(id_buscar, opcion_datos):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id FROM datos_personales WHERE id = %s;", (id_buscar,))
        if not cursor.fetchone():
            return None

        if "1." in opcion_datos:
            sql = """
                SELECT p.nombre, p.apellidos, p.telefono, p.correo, h.tipo_sangre, h.alergias, 
                       c.nombre_contacto, m.diagnostico, s.temperatura 
                FROM datos_personales p
                LEFT JOIN historial_clinico h ON p.id = h.paciente_id
                LEFT JOIN contactos_emergencia c ON p.id = c.paciente_id
                LEFT JOIN consultas_medicas m ON p.id = m.paciente_id
                LEFT JOIN signos_vitales s ON p.id = s.paciente_id
                WHERE p.id = %s;
            """
        elif "2." in opcion_datos:
            sql = "SELECT nombre FROM datos_personales WHERE id = %s;"
        elif "3." in opcion_datos:
            sql = "SELECT correo FROM datos_personales WHERE id = %s;"
        else:
            sql = "SELECT nombre, correo FROM datos_personales WHERE id = %s;"

        cursor.execute(sql, (id_buscar,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()


def eliminar_paciente(id_eliminar):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id FROM datos_personales WHERE id = %s;", (id_eliminar,))
        if not cursor.fetchone():
            return False

        cursor.execute("DELETE FROM historial_clinico WHERE paciente_id = %s;", (id_eliminar,))
        cursor.execute("DELETE FROM contactos_emergencia WHERE paciente_id = %s;", (id_eliminar,))
        cursor.execute("DELETE FROM consultas_medicas WHERE paciente_id = %s;", (id_eliminar,))
        cursor.execute("DELETE FROM signos_vitales WHERE paciente_id = %s;", (id_eliminar,))
        cursor.execute("DELETE FROM datos_personales WHERE id = %s;", (id_eliminar,))

        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()


def actualizar_paciente(id_actualizar, columna, nuevo_valor):
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id FROM datos_personales WHERE id = %s;", (id_actualizar,))
        if not cursor.fetchone():
            return False

        columnas_validas = ["nombre", "apellidos", "telefono", "correo"]
        if columna not in columnas_validas:
            return False

        sql = f"UPDATE datos_personales SET {columna} = %s WHERE id = %s;"
        cursor.execute(sql, (nuevo_valor, id_actualizar))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()
def guardar_ruta_archivo(cedula, nombre_doc, ruta):
    """Guarda en MySQL la ubicación del archivo copiado al Escritorio"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        sql = "INSERT INTO expedientes_digitales (paciente_id, nombre_documento, ruta_local) VALUES (%s, %s, %s);"
        cursor.execute(sql, (cedula, nombre_doc, ruta))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()
#nueva parte

def buscar_archivos_paciente(cedula):
    """Busca todos los documentos adjuntos que tiene una cédula"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        sql = "SELECT nombre_documento, ruta_local FROM expedientes_digitales WHERE paciente_id = %s;"
        cursor.execute(sql, (cedula,))
        return cursor.fetchall() # Devuelve la lista de archivos encontrados
    finally:
        cursor.close()
        conexion.close()
