from config import app
from flask import render_template, request, jsonify
import psycopg2
import os
from io import BytesIO
from PIL import Image
import base64
import subprocess
import csv
import joblib
import pandas as pd

# Cargar el modelo entrenado de SVM
model_path = 'data/results/best_svm_model.pkl'
svm_model = joblib.load(model_path)

# Función para manejar datos de texto de forma segura
def safe_str(input_str):
    if isinstance(input_str, str):
        return input_str.encode('utf-8', 'replace').decode('utf-8')
    return input_str

# Ruta para la página de predicción TDAH
@app.route("/prediccion_tdah")
def prediccion_tdah():
    try:
        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        cur.execute("SELECT id_expresion, nombre FROM expresiones")
        expresiones = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("prediccion_tdah.html", expresiones=expresiones)
    except Exception as e:
        print(f"Error al obtener las expresiones: {e}")
        return render_template("prediccion_tdah.html", expresiones=[])

# Ruta para manejar la captura de imágenes en predicción TDAH
@app.route('/api/predict_capture_images', methods=['POST'])
def handle_predict_capture_images():
    try:
        data = request.get_json()
        nombre = safe_str(data.get('nombre'))
        edad = int(data.get('edad'))
        genero = safe_str(data.get('genero'))
        expresion = safe_str(data.get('expresion'))

        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        cur.execute(
            "SELECT id_estudiante FROM estudiantes WHERE nombre = %s AND edad = %s AND genero = %s", 
            (nombre, edad, genero)
        )
        estudiante_existente = cur.fetchone()

        if estudiante_existente:
            id_estudiante = estudiante_existente[0]
        else:
            cur.execute(
                "INSERT INTO estudiantes (nombre, edad, genero) VALUES (%s, %s, %s) RETURNING id_estudiante", 
                (nombre, edad, genero)
            )
            id_estudiante = cur.fetchone()[0]
            conn.commit()

        cur.execute("SELECT id_expresion FROM expresiones WHERE nombre = %s", (expresion,))
        expresion_row = cur.fetchone()

        if expresion_row is None:
            return jsonify({'success': False, 'message': f'La expresión "{expresion}" no existe en la base de datos.'})

        id_expresion = expresion_row[0]

        image_data = data.get('imagen')
        image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

        output_dir = f"data/predict_raw/{id_estudiante}/{expresion}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        img_count = len(os.listdir(output_dir)) + 1
        image_name = f"{id_estudiante}_{expresion}_captura_{img_count}.jpg"
        image.save(f"{output_dir}/{image_name}")

        cur.execute(
            """
            INSERT INTO resultados_facial (id_estudiante, id_expresion, nombre_imagen, success)
            VALUES (%s, %s, %s, %s)
            """, 
            (id_estudiante, id_expresion, image_name, True)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Imagen capturada y guardada correctamente.'})
    except Exception as e:
        print(f"Error durante la captura de imágenes: {e}")
        return jsonify({'success': False, 'message': f'Error en la captura de imágenes: {e}'})

# Ruta para manejar el procesamiento de imágenes usando OpenFace y predicción
@app.route('/api/process_openface_and_predict', methods=['POST'])
def handle_process_openface_and_predict():
    try:
        data = request.get_json()
        nombre = safe_str(data.get('nombre'))
        edad = int(data.get('edad'))
        genero = safe_str(data.get('genero'))

        conn = psycopg2.connect(
            dbname="Test1",
            user="postgres",
            password="123",
            host="localhost",
            options='-c client_encoding=UTF8'
        )
        cur = conn.cursor()

        cur.execute(
            "SELECT id_estudiante FROM estudiantes WHERE nombre = %s AND edad = %s AND genero = %s",
            (nombre, edad, genero)
        )
        estudiante = cur.fetchone()
        if not estudiante:
            return jsonify({'success': False, 'message': 'Estudiante no encontrado en la base de datos.'})

        id_estudiante = estudiante[0]

        process_student_images_for_prediction(str(id_estudiante))

        result = predict_tdah_for_student(str(id_estudiante))

        return jsonify({'success': True, 'prediccion': result})
    except Exception as e:
        print(f"Error en el procesamiento de imágenes o predicción: {e}")
        return jsonify({'success': False, 'message': f'Error en el procesamiento o predicción: {e}'})

def process_student_images_for_prediction(student_id, input_dir='data/predict_raw', output_dir='data/predict_results'):
    student_dir = os.path.join(input_dir, str(student_id))  # Convertir student_id a cadena
    if not os.path.exists(student_dir):
        print(f"No se encontraron imágenes para el estudiante {student_id}")
        return

    results_student_dir = os.path.join(output_dir, str(student_id))  # Convertir student_id a cadena
    if not os.path.exists(results_student_dir):
        os.makedirs(results_student_dir)

    for expression in os.listdir(student_dir):
        expression_dir = os.path.join(student_dir, expression)
        csv_path = os.path.join(results_student_dir, f'{expression}_results.csv')
        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Image', 'Expresion', 'timestamp', 'confidence', 'success', 
                             'AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 
                             'AU10_r', 'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 'AU23_r', 
                             'AU25_r', 'AU26_r', 'AU45_r', 'AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 
                             'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 'AU15_c', 
                             'AU17_c', 'AU20_c', 'AU23_c', 'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c'])

            for image_name in os.listdir(expression_dir):
                image_path = os.path.join(expression_dir, image_name)
                temp_csv = os.path.join('openface_output', 'temp_output.csv')
                run_openface(image_path, temp_csv)

                with open(temp_csv, mode='r') as temp_file:
                    reader = csv.reader(temp_file)
                    next(reader)
                    for row in reader:
                        writer.writerow([image_name, expression] + row[2:])

                os.remove(temp_csv)

def run_openface(image_path, output_csv):
    openface_executable = 'OpenFace_2.2.0_win_x64/FeatureExtraction.exe'
    command = [
        openface_executable,
        '-f', image_path,
        '-aus',
        '-of', output_csv
    ]
    subprocess.run(command, check=True)

def predict_tdah_for_student(student_id, output_dir='data/predict_results'):
    results_dir = os.path.join(output_dir, student_id)
    data_frames = []

    # Leer todos los archivos CSV de resultados en el directorio del estudiante
    for expression_file in os.listdir(results_dir):
        if expression_file.endswith('_results.csv'):
            csv_path = os.path.join(results_dir, expression_file)
            df = pd.read_csv(csv_path)
            data_frames.append(df)

    # Concatenar todos los datos en un solo DataFrame
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Asegurarse de que los nombres de las columnas coincidan en formato
    combined_data.columns = [col.lower() for col in combined_data.columns]
    combined_data = pd.get_dummies(combined_data, columns=['expresion'], drop_first=True)

    # Filtrar las columnas necesarias para la predicción
    AU_columns = [col for col in combined_data.columns if col.startswith('au')]
    expression_columns = [col for col in combined_data.columns if col.startswith('expresion_')]
    X = combined_data[AU_columns + expression_columns]

    # Alinear X con las características esperadas por el modelo y rellenar con ceros cualquier columna faltante
    expected_columns = svm_model.feature_names_in_
    X = X.reindex(columns=expected_columns, fill_value=0)

    # Realizar la predicción
    prediction = svm_model.predict(X)

    # Interpretar el resultado de la predicción
    return "Tiene TDAH" if prediction.mean() >= 0.5 else "No tiene TDAH"