from config import app
from controllers.indexController import index

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/", view_func=index)
