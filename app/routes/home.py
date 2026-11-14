from flask import Blueprint, render_template

# Intentamos importar los modelos de forma segura por si aún no existen en esta fase
try:
  from app.models.libro import Libro
  from app.models.lector import Lector
  from app.models.prestamo import Prestamo
except ImportError:
  Libro = Lector = Prestamo = None

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
  # Contadores seguros en caso de que las tablas no estén creadas aún
  total_libros = Libro.query.count() if Libro else 0
  total_lectores = Lector.query.count() if Lector else 0
  total_prestamos = Prestamo.query.count() if Prestamo else 0

  return render_template(
      "index.html",
      libros=total_libros,
      lectores=total_lectores,
      prestamos=total_prestamos,
  )