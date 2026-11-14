import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv 

#Cargar las variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Registrar Blueprint del Home
from app.routes.home import home_bp

app.register_blueprint(home_bp)

with app.app_context():
    try:
      from app.models import libro, lector, prestamo  # noqa: F401
    except ImportError:
      pass

    db.create_all()
