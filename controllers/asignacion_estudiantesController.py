from config import app
from flask import render_template

# Ruta para la página de inicio
@app.route("/asignacion_estudiantes")
def asignacion_estudiantes():
    
    # Renderizamos la plantilla y pasamos los datos a la misma
    return render_template("asignacion_estudiantes.html")