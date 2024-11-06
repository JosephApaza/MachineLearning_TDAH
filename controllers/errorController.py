from config import app
from flask import render_template, redirect, url_for

# Ruta para manejar errores 400
@app.errorhandler(400)
def page_not_found(e):
    # Redirige a la página personalizada de error 400
    return redirect(url_for('error_400'))

# Ruta para manejar errores 404
@app.errorhandler(404)
def page_not_found(e):
    # Redirige a la página personalizada de error 404
    return redirect(url_for('error_404'))

# Ruta para la página de error 404
@app.route('/error_404')
def error_404():
    # Renderiza la plantilla HTML correspondiente a la página de error 404
    return render_template('404.html')

# Ruta para la página de error 404
@app.route('/error_400')
def error_400():
    # Renderiza la plantilla HTML correspondiente a la página de error 400
    return render_template('400.html')