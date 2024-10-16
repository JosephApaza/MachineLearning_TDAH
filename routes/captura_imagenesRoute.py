from config import app
from controllers.captura_imagenesController import captura_imagenes

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/captura_imagenes", view_func=captura_imagenes)
