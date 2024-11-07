from config import app
from controllers.prediccion_tdahController import prediccion_tdah

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/prediccion_tdah", view_func=prediccion_tdah)
