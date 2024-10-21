import csv
from config import app
from flask import render_template, jsonify
import psycopg2
import os
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

            # Definir directorio donde se guardan los resultados
            output_dir = f"data/results/{id_estudiante}"

            # Comprobar si ya se procesaron todas las expresiones
            todas_expresiones_procesadas = True
            for expression in os.listdir(f"data/raw/{id_estudiante}"):
                csv_path = os.path.join(output_dir, expression, f'{expression}_results.csv')
                if not os.path.exists(csv_path):
                    todas_expresiones_procesadas = False
                    break

            # Si todas las expresiones ya están procesadas, saltar
            if todas_expresiones_procesadas:
                print(f"Estudiante {nombre} ({id_estudiante}) ya tiene todas las expresiones procesadas. Saltando.")
                continue

            # Procesar las imágenes del estudiante con el script de OpenFace
            process_student_images(str(id_estudiante), tdah)

            # Leer el archivo CSV generado por OpenFace
            for expression in os.listdir(f"data/raw/{id_estudiante}"):
                csv_path = os.path.join(output_dir, expression, f'{expression}_results.csv')

                if os.path.exists(csv_path):
                    with open(csv_path, mode='r') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            # Obtener los datos necesarios del CSV usando las claves en mayúsculas
                            confidence = float(row.get('confidence', 0))  # Usar 0 si no está disponible
                            au_values = {key: row.get(key, 0) for key in row if key.startswith('AU')}  # AUs en mayúsculas
                            nombre_imagen = row.get('Image', 'desconocida')  # Usar 'desconocida' si no está disponible

                            # Actualizar los resultados en la base de datos
                            cur.execute("""
                                UPDATE resultados_facial 
                                SET nombre_imagen = %s, confidence = %s, 
                                    au01_r = %s, au02_r = %s, au04_r = %s, au05_r = %s, 
                                    au06_r = %s, au07_r = %s, au09_r = %s, au10_r = %s, 
                                    au12_r = %s, au14_r = %s, au15_r = %s, au17_r = %s, 
                                    au20_r = %s, au23_r = %s, au25_r = %s, au26_r = %s, 
                                    au45_r = %s, 
                                    au01_c = %s, au02_c = %s, au04_c = %s, au05_c = %s, 
                                    au06_c = %s, au07_c = %s, au09_c = %s, au10_c = %s, 
                                    au12_c = %s, au14_c = %s, au15_c = %s, au17_c = %s, 
                                    au20_c = %s, au23_c = %s, au25_c = %s, au26_c = %s, 
                                    au28_c = %s, au45_c = %s
                                WHERE id_estudiante = %s AND id_expresion = (SELECT id_expresion FROM expresiones WHERE nombre = %s)
                                """, 
                                (
                                    nombre_imagen, 
                                    confidence,
                                    au_values.get('AU01_r', 0), au_values.get('AU02_r', 0), au_values.get('AU04_r', 0), au_values.get('AU05_r', 0),
                                    au_values.get('AU06_r', 0), au_values.get('AU07_r', 0), au_values.get('AU09_r', 0), au_values.get('AU10_r', 0),
                                    au_values.get('AU12_r', 0), au_values.get('AU14_r', 0), au_values.get('AU15_r', 0), au_values.get('AU17_r', 0),
                                    au_values.get('AU20_r', 0), au_values.get('AU23_r', 0), au_values.get('AU25_r', 0), au_values.get('AU26_r', 0),
                                    au_values.get('AU45_r', 0),
                                    au_values.get('AU01_c', 0), au_values.get('AU02_c', 0), au_values.get('AU04_c', 0), au_values.get('AU05_c', 0),
                                    au_values.get('AU06_c', 0), au_values.get('AU07_c', 0), au_values.get('AU09_c', 0), au_values.get('AU10_c', 0),
                                    au_values.get('AU12_c', 0), au_values.get('AU14_c', 0), au_values.get('AU15_c', 0), au_values.get('AU17_c', 0),
                                    au_values.get('AU20_c', 0), au_values.get('AU23_c', 0), au_values.get('AU25_c', 0), au_values.get('AU26_c', 0),
                                    au_values.get('AU28_c', 0), au_values.get('AU45_c', 0),
                                    id_estudiante, expression  # Los identificadores para la fila
                                )
                            )
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Procesamiento de expresiones completado.'})

    except Exception as e:
        print(f"Error durante el procesamiento de expresiones: {e}")
        return jsonify({'success': False, 'message': f'Error en el procesamiento: {e}'})
