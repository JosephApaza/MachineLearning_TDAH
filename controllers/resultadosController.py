from config import app, db
from flask import render_template
from sqlalchemy import text

# Ruta para la página de inicio
@app.route("/resultados")
def resultados():
    # Ejecutar el procedimiento almacenado directamente
    estudiantes = db.session.execute(text("SELECT * FROM listar_estudiantes()")).fetchall()

    # Renderizamos la plantilla y pasamos los datos a la misma
    return render_template("resultados.html", estudiantes=estudiantes)