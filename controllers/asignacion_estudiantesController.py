from config import app, db
from flask import render_template
from sqlalchemy import text

# Ruta para la página de inicio
@app.route("/asignacion_estudiantes", methods=['POST'])
def asignacion_estudiantes():
    # Ejecutar el procedimiento almacenado directamente
    estudiantes = db.session.execute(text("SELECT * FROM listar_estudiantes()")).fetchall()

    # Renderizar la plantilla con la lista de estudiantes
    return render_template('asignacion_estudiantes.html', estudiantes=estudiantes)