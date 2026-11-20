
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bibliotech-clave-local-2026'

# Configuración de la base de datos
database_url = os.getenv("DATABASE_URL")

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca_local.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Registrar Blueprint del Home
from app.routes.home import home_bp
app.register_blueprint(home_bp)

# Registrar Blueprint de Préstamos
from app.routes.prestamos import prestamos_bp
app.register_blueprint(prestamos_bp)

# Importar modelos y crear tablas
with app.app_context():
    try:
        from app.models import libro, lector, prestamo
    except ImportError:
        pass

    db.create_all()
