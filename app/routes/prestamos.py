
from flask import Blueprint, render_template

prestamos_bp = Blueprint("prestamos", __name__)


@prestamos_bp.route("/prestamos")
def index():
    return render_template("prestamos/index.html")
