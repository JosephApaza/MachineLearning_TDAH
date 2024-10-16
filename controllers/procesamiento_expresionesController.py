from config import app
from flask import render_template

# Ruta para la página de inicio
@app.route("/procesamiento_expresiones")
def procesamiento_expresiones():
    
    # Renderizamos la plantilla y pasamos los datos a la misma
    return render_template("procesamiento_expresiones.html")