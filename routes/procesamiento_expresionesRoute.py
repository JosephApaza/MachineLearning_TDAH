from config import app
from controllers.procesamiento_expresionesController import procesamiento_expresiones

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/procesamiento_expresiones", view_func=procesamiento_expresiones)
