from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="views")

# Configurar SQLAlchemy con PostgreSQL usando utf-8
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost/Test1?client_encoding=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Asegurarse de que Flask maneje correctamente JSON con caracteres especiales
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

# Importar las rutas
from routes.indexRoute import *
from routes.captura_imagenesRoute import *
from routes.asignacion_estudiantesRoute import *
from routes.procesamiento_expresionesRoute import *
from routes.resultadosRoute import *
from routes.editar_estudianteRoute import *
from routes.errorRoute import *