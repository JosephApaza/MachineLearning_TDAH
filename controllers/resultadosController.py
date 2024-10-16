from config import app
from flask import render_template

# Ruta para la página de inicio
@app.route("/resultados")
def resultados():
    
    # Renderizamos la plantilla y pasamos los datos a la misma
    return render_template("resultados.html")