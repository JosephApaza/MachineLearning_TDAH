from config import app
from controllers.editar_estudianteController import editar_estudiante

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/editar_estudiante/<int:id>", view_func=editar_estudiante)
