import pandas as pd

def analyze_openface_output(csv_path):
    # Cargar los resultados del CSV generado por OpenFace
    df = pd.read_csv(csv_path)

    # Filtrar las columnas que contienen los Action Units
    au_columns = [col for col in df.columns if 'AU' in col]
    au_values = df[au_columns].mean()  # Calcular el promedio de los AUs

    print("Promedio de Action Units detectados:")
    print(au_values)

    return au_values

# Ejemplo de uso
if __name__ == '__main__':
    csv_path = 'openface_output/output.csv'  # Ruta del archivo CSV generado
    analyze_openface_output(csv_path)
