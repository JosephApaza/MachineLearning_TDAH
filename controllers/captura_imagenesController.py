from config import app
from flask import render_template, request, jsonify
import psycopg2
from io import BytesIO
from PIL import Image
import base64
import os

# Función para manejar datos de texto de forma segura (evita problemas de codificación)
def safe_str(input_str):
    if isinstance(input_str, str):
        return input_str.encode('utf-8', 'replace').decode('utf-8')
    return input_str

# Ruta para la página de captura de imágenes
@app.route("/captura_imagenes")
def captura_imagenes():
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

        # Obtener las expresiones disponibles desde la base de datos
        cur.execute("SELECT id_expresion, nombre FROM expresiones")
        expresiones = cur.fetchall()

        # Cerrar la conexión
        cur.close()
        conn.close()

        # Renderizar la plantilla HTML y pasar las expresiones
        return render_template("captura_imagenes.html", expresiones=expresiones)
    except Exception as e:
        print(f"Error al obtener las expresiones: {e}")
        return render_template("captura_imagenes.html", expresiones=[])

# Ruta para manejar la solicitud de captura de imágenes
@app.route('/api/capture_images', methods=['POST'])
def handle_capture_images():
    try:
        # Obtener los datos enviados desde el frontend
        data = request.get_json()

        # Sanitizar los datos recibidos
        nombre = safe_str(data.get('nombre'))
        edad = int(data.get('edad'))
        genero = safe_str(data.get('genero'))
        tiene_tdah = data.get('tdah')
        expresion = safe_str(data.get('expresion'))

        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        # Verificar si el estudiante ya existe basado en nombre, edad, y género
        cur.execute(
            "SELECT id_estudiante FROM estudiantes WHERE nombre = %s AND edad = %s AND genero = %s", 
            (nombre, edad, genero)
        )
        estudiante_existente = cur.fetchone()

        if estudiante_existente:
            # Si el estudiante ya existe, obtener su ID
            id_estudiante = estudiante_existente[0]
        else:
            # Si el estudiante no existe, insertarlo y obtener el ID generado
            cur.execute(
                "INSERT INTO estudiantes (nombre, edad, genero, tiene_tdah) VALUES (%s, %s, %s, %s) RETURNING id_estudiante", 
                (nombre, edad, genero, tiene_tdah)
            )
            id_estudiante = cur.fetchone()[0]
            conn.commit()

        # Consultar ID de la expresión
        cur.execute("SELECT id_expresion FROM expresiones WHERE nombre = %s", (expresion,))
        expresion_row = cur.fetchone()

        if expresion_row is None:
            return jsonify({'success': False, 'message': f'La expresión "{expresion}" no existe en la base de datos.'})

        id_expresion = expresion_row[0]

        # Verificar si ya existe un registro en resultados_facial para este estudiante y expresión
        cur.execute(
            "SELECT id_resultados, cant_imagen FROM resultados_facial WHERE id_estudiante = %s AND id_expresion = %s", 
            (id_estudiante, id_expresion)
        )
        resultado_facial = cur.fetchone()

        if resultado_facial:
            # Si ya existe un registro, actualizar el campo cant_imagen
            id_resultados, cant_imagen_actual = resultado_facial
            cant_imagen_nueva = cant_imagen_actual + 1
            cur.execute(
                "UPDATE resultados_facial SET cant_imagen = %s, frame = %s WHERE id_resultados = %s",
                (cant_imagen_nueva, cant_imagen_nueva, id_resultados)
            )
        else:
            # Si no existe un registro, crear uno nuevo
            cur.execute(
                """
                INSERT INTO resultados_facial (id_estudiante, id_expresion, cant_imagen, frame, success)
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (id_estudiante, id_expresion, 1, 1, True)
            )

        # Decodificar la imagen en base64
        image_data = data.get('imagen')
        image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

        # Crear el directorio si no existe
        output_dir = f"data/raw/{id_estudiante}/{expresion}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar la imagen
        img_count = len(os.listdir(output_dir)) + 1
        image.save(f"{output_dir}/{expresion}_captura_{img_count}.jpg")

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Imagen capturada y guardada correctamente.'})
    except Exception as e:
        print(f"Error durante la captura de imágenes: {e}")
        return jsonify({'success': False, 'message': f'Error en la captura de imágenes: {e}'})
