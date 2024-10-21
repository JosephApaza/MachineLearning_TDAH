from config import app
from flask import render_template, jsonify
import psycopg2
from process_with_openface import process_student_images  # Importar el script para procesar con OpenFace


# Ruta para la página de procesamiento de expresiones
@app.route("/procesamiento_expresiones")
def procesamiento_expresiones():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        # Llamar al procedimiento almacenado para obtener los datos
        cur.execute("SELECT * FROM obtener_datos_estudiantes()")
        estudiantes_datos = cur.fetchall()

        cur.close()
        conn.close()

        # Renderizar la plantilla con los datos obtenidos
        return render_template("procesamiento_expresiones.html", estudiantes_datos=estudiantes_datos)

    except Exception as e:
        print(f"Error al obtener los datos de los estudiantes: {e}")
        return render_template("procesamiento_expresiones.html", estudiantes_datos=[])


# Ruta para manejar el procesamiento de expresiones
@app.route('/api/procesar_expresiones', methods=['POST'])
def handle_procesar_expresiones():
    try:
        # Conectar a la base de datos para obtener los datos de los estudiantes
        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        # Obtener los estudiantes que tienen imágenes capturadas
        cur.execute("SELECT id_estudiante, nombre, edad, genero, tiene_tdah FROM estudiantes")
        estudiantes = cur.fetchall()

        # Procesar las imágenes de cada estudiante
        for estudiante in estudiantes:
            id_estudiante, nombre, edad, genero, tiene_tdah = estudiante

            # Convertir el valor booleano de TDAH a una cadena "True" o "False" para el procesamiento
            tdah = "True" if tiene_tdah else "False"

            # Procesar las imágenes del estudiante con el script de OpenFace
            process_student_images(str(id_estudiante), tdah)

        cur.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Procesamiento de expresiones completado.'})

    except Exception as e:
        print(f"Error durante el procesamiento de expresiones: {e}")
        return jsonify({'success': False, 'message': f'Error en el procesamiento: {e}'})
