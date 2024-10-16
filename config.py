from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="views")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/tdah_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes.indexRoute import *
from routes.captura_imagenesRoute import *
from routes.asignacion_estudiantesRoute import *
from routes.procesamiento_expresionesRoute import *
from routes.resultadosRoute import *