import cv2
import os

def capture_images(student_id, output_dir='data/raw'):
    # Crear el directorio de salida si no existe
    output_path = os.path.join(output_dir, student_id)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Iniciar captura de video (cámara predeterminada)
    cap = cv2.VideoCapture(0)
    count = 0

    while count < 100:  # Limitar la captura a 100 imágenes
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara")
            break

        # Guardar cada imagen con un nombre numerado
        img_path = os.path.join(output_path, f'face_{count}.jpg')
        cv2.imwrite(img_path, frame)
        count += 1

        # Mostrar la imagen capturada en pantalla
        cv2.imshow('Capturando imágenes', frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f'Captura completada. {count} imágenes guardadas en {output_path}')

# Ejemplo de uso
if __name__ == '__main__':
    student_id = input("Introduce el ID del estudiante: ")
    capture_images(student_id)
