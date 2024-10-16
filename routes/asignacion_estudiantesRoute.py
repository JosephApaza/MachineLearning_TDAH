from config import app
from controllers.asignacion_estudiantesController import asignacion_estudiantes

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/asignacion_estudiantes", view_func=asignacion_estudiantes)
