import time
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC
import numpy as np

# Cargar los datos
data = pd.read_csv('data/results/svm_data.csv')

# Ver la distribución de clases
print("Distribución de clases en todo el dataset:")
print(data['tiene_tdah'].value_counts())

# Transformar las variables categóricas (genero_estudiante y expresion) a variables numéricas
data_encoded = pd.get_dummies(data, columns=['genero_estudiante', 'expresion'], drop_first=True)

# Preparar los datos para el entrenamiento
X = data_encoded.drop(columns=['tiene_tdah', 'nombre_estudiante', 'nombre_imagen', 'fecha'])  # Variables de entrada
y = data_encoded['tiene_tdah']  # Variable de salida

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Ver la distribución de clases en el conjunto de entrenamiento
print("\nDistribución de clases en el conjunto de entrenamiento:")
print(y_train.value_counts())

# Definir los parámetros para Grid Search
param_grid = {
    'C': [0.1, 1, 10, 100],
    'kernel': ['linear', 'rbf'],
    'gamma': [0.1, 1, 'scale'],
}

# Crear el modelo SVM
svm_model = SVC(probability=True)

# Realizar Grid Search con validación cruzada
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy')

# Medir el tiempo de procesamiento
start_time = time.time()
grid_search.fit(X_train, y_train)
end_time = time.time()

# Resultados de Grid Search
print(f"\nTiempo de procesamiento: {end_time - start_time:.2f} segundos")
print("Mejores parámetros encontrados:", grid_search.best_params_)

# Evaluar el mejor modelo en el conjunto de prueba
best_svm_model = grid_search.best_estimator_
y_pred = best_svm_model.predict(X_test)

# Reporte de clasificación y matriz de confusión
print("\nPrecisión en el conjunto de prueba:", accuracy_score(y_test, y_pred) * 100)
print("Matriz de confusión:\n", confusion_matrix(y_test, y_pred))
print("Reporte de clasificación:\n", classification_report(y_test, y_pred))

# Calcular el AUC (Área bajo la curva ROC)
y_pred_proba = best_svm_model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f"ROC AUC: {roc_auc:.2f}")

# --- Realizar múltiples iteraciones para evaluar la estabilidad ---
num_iterations = 10
accuracies = []

for i in range(num_iterations):
    # Dividir los datos de nuevo para cada iteración
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i, stratify=y)
    
    # Entrenar el modelo con los mejores parámetros obtenidos
    best_svm_model.fit(X_train, y_train)
    
    # Hacer predicciones y calcular la precisión
    y_pred = best_svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)
    
    print(f"Iteración {i+1} - Precisión: {accuracy * 100:.2f}%")

# Calcular y mostrar la precisión promedio después de todas las iteraciones
average_accuracy = np.mean(accuracies)
print(f"\nPrecisión promedio después de {num_iterations} iteraciones: {average_accuracy * 100:.2f}%")
