from config import app
from controllers.resultadosController import resultados

# Agrega una regla de URL para la página de inicio ("/") y asigna la función del controlador correspondiente
app.add_url_rule("/resultados", view_func=resultados)
