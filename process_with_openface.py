import subprocess
import os
import csv

def run_openface(image_path, output_csv):
    # Ruta al ejecutable de OpenFace (ajústalo a donde descomprimiste OpenFace)
    openface_executable = 'OpenFace_2.2.0_win_x64/FeatureExtraction.exe'

    # Comando para ejecutar OpenFace
    command = [
        openface_executable,        # Ruta a FeatureExtraction.exe
        '-f', image_path,           # Ruta de la imagen
        '-aus',                     # Extraer Action Units
        '-of', output_csv           # Archivo CSV donde guardar los resultados de OpenFace
    ]

    # Ejecutar el comando usando subprocess
    subprocess.run(command)

# Procesar todas las imágenes de un estudiante
def process_student_images(student_id, tdah, input_dir='data/raw', output_dir='data/results'):
    student_dir = os.path.join(input_dir, student_id)
    if not os.path.exists(student_dir):
        print(f"No se encontraron imágenes para el estudiante {student_id}")
        return

    # Crear el directorio de resultados para este estudiante si no existe
    results_student_dir = os.path.join(output_dir, student_id)
    if not os.path.exists(results_student_dir):
        os.makedirs(results_student_dir)

    # Procesar cada expresión del estudiante
    for expression in os.listdir(student_dir):
        expression_dir = os.path.join(student_dir, expression)

        # Crear el directorio de resultados de la expresión dentro de results/{student_id}/{expression}
        results_expression_dir = os.path.join(results_student_dir, expression)
        if not os.path.exists(results_expression_dir):
            os.makedirs(results_expression_dir)

        # Crear el CSV de resultados en la carpeta de la expresión
        csv_path = os.path.join(results_expression_dir, f'{expression}_results.csv')
        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Escribir encabezado del CSV
            writer.writerow(['Image', 'TDAH', 'Expresion', 'AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 
                             'AU09_r', 'AU10_r', 'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 
                             'AU23_r', 'AU25_r', 'AU26_r', 'AU45_r', 'AU01_c', 'AU02_c', 'AU04_c', 
                             'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 
                             'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 'AU25_c', 'AU26_c', 'AU28_c', 
                             'AU45_c'])  # Añadir "Expresion" al encabezado

            # Procesar cada imagen en el directorio de la expresión
            for image_name in os.listdir(expression_dir):
                image_path = os.path.join(expression_dir, image_name)
                print(f"Procesando {image_path}...")

                # Ejecutar OpenFace y guardar resultados en un CSV temporal
                temp_csv = os.path.join('openface_output', 'temp_output.csv')
                run_openface(image_path, temp_csv)

                # Leer el CSV generado por OpenFace
                with open(temp_csv, mode='r') as temp_file:
                    reader = csv.reader(temp_file)
                    next(reader)  # Saltar encabezado
                    for row in reader:
                        # Agregar el nombre de la imagen, si tiene TDAH, y la expresión al inicio de la fila
                        writer.writerow([image_name, tdah, expression] + row[2:])  # Agregar expresión

                # Eliminar archivo temporal después de usarlo
                os.remove(temp_csv)

        print(f"Resultados guardados en {csv_path}")
