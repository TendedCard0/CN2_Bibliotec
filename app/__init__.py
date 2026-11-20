import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-bibliotec")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///biblioteca_local.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.home import home_bp
    from app.routes.lectores import lectores_bp
    from app.routes.prestamos import prestamos_bp
    from app.routes.libros import libros_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(lectores_bp)
    app.register_blueprint(prestamos_bp)
    app.register_blueprint(libros_bp)

    with app.app_context():
        from app.models.lector import Lector
        from app.models.libro import Libro
        from app.models.prestamo import Prestamo
        db.create_all()

    return app