import subprocess
import os

def run_openface(image_path, output_dir='openface_output/'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta al ejecutable de OpenFace (ajústalo a donde descomprimiste OpenFace)
    openface_executable = 'OpenFace_2.2.0_win_x64/FeatureExtraction.exe'

    # Comando para ejecutar OpenFace
    command = [
        openface_executable,        # Ruta a FeatureExtraction.exe
        '-f', image_path,           # Ruta de la imagen
        '-aus',                     # Extraer Action Units
        '-of', os.path.join(output_dir, 'output.csv')  # Archivo CSV donde guardar los resultados
    ]

    # Ejecutar el comando usando subprocess
    subprocess.run(command)

# Procesar todas las imágenes de un estudiante
def process_student_images(student_id, input_dir='data/raw', output_dir='openface_output'):
    student_dir = os.path.join(input_dir, student_id)
    if not os.path.exists(student_dir):
        print(f"No se encontraron imágenes para el estudiante {student_id}")
        return

    # Procesar cada imagen del estudiante con OpenFace
    for image_name in os.listdir(student_dir):
        image_path = os.path.join(student_dir, image_name)
        print(f"Procesando {image_path}...")
        run_openface(image_path, output_dir)

# Ejemplo de uso
if __name__ == '__main__':
    student_id = input("Introduce el ID del estudiante para procesar: ")
    process_student_images(student_id)
