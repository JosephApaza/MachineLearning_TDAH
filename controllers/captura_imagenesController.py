from config import app
from flask import render_template

# Ruta para la página de inicio
@app.route("/captura_imagenes")
def captura_imagenes():
    
    # Renderizamos la plantilla y pasamos los datos a la misma
    return render_template("captura_imagenes.html")