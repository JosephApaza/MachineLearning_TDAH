from config import app, db
from flask import render_template, request
from sqlalchemy import text

# Ruta para la página de inicio
@app.route("/editar_estudiante/<int:id_estudiante>", methods=['GET', 'POST'])
def editar_estudiante(id_estudiante):
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        genero = request.form['genero']
        tiene_tdah = 'tiene_tdah' in request.form  # Checkbox

        # Llamada al procedimiento almacenado de PostgreSQL
        sql = text("CALL actualizar_estudiante(:id_estudiante, :nombre, :edad, :genero, :tiene_tdah)")
        db.session.execute(sql, {'id_estudiante': id_estudiante, 'nombre': nombre, 'edad': edad, 'genero': genero, 'tiene_tdah': tiene_tdah})
        db.session.commit()
    
    # Obtener el estudiante para prellenar el formulario
    estudiante = db.session.execute(text(f"SELECT * FROM estudiantes WHERE id_estudiante = :id_estudiante"), {'id_estudiante': id_estudiante}).fetchone()
    return render_template('editar_estudiante.html', estudiante=estudiante)