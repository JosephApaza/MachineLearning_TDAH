from config import app
from controllers.errorController import *

# Agrega una regla de URL para manejar errores 400 (Bad Request)
app.add_url_rule("/error_400", view_func=error_400)

# Agrega una regla de URL para manejar errores 404 (Not Found)
app.add_url_rule("/error_404", view_func=error_404)