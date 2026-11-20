
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.libro import Libro
from app.models.lector import Lector
from app.models.prestamo import Prestamo

prestamos_bp = Blueprint("prestamos", __name__)


@prestamos_bp.route("/prestamos")
def index():
    prestamos = Prestamo.query.order_by(Prestamo.id.desc()).all()
    libros = Libro.query.order_by(Libro.titulo.asc()).all()
    lectores = Lector.query.order_by(Lector.nombre.asc()).all()

    return render_template(
        "prestamos/index.html",
        prestamos=prestamos,
        libros=libros,
        lectores=lectores
    )


@prestamos_bp.route("/prestamos/registrar", methods=["POST"])
def registrar():
    try:
        libro_id = int(request.form["libro_id"])
        lector_id = int(request.form["lector_id"])
        fecha = datetime.strptime(
            request.form["fecha_prestamo"], "%Y-%m-%d"
        ).date()

        if not db.session.get(Libro, libro_id) or not db.session.get(Lector, lector_id):
            flash("Selecciona un libro y un lector válidos.", "danger")
            return redirect(url_for("prestamos.index"))

        prestamo = Prestamo(
            libro_id=libro_id,
            lector_id=lector_id,
            fecha_prestamo=fecha,
            estado="Prestado"
        )

        db.session.add(prestamo)
        db.session.commit()
        flash("Préstamo registrado correctamente.", "success")

    except (ValueError, KeyError):
        db.session.rollback()
        flash("Verifica los datos del préstamo.", "danger")

    return redirect(url_for("prestamos.index"))


@prestamos_bp.route("/prestamos/editar/<int:id>", methods=["POST"])
def editar(id):
    prestamo = db.session.get(Prestamo, id)

    if not prestamo:
        flash("Préstamo no encontrado.", "danger")
        return redirect(url_for("prestamos.index"))

    try:
        libro_id = int(request.form["libro_id"])
        lector_id = int(request.form["lector_id"])

        if not db.session.get(Libro, libro_id) or not db.session.get(Lector, lector_id):
            raise ValueError("Libro o lector inválido")

        prestamo.libro_id = libro_id
        prestamo.lector_id = lector_id
        prestamo.fecha_prestamo = datetime.strptime(
            request.form["fecha_prestamo"], "%Y-%m-%d"
        ).date()

        fecha_devolucion = request.form.get("fecha_devolucion")
        prestamo.fecha_devolucion = (
            datetime.strptime(fecha_devolucion, "%Y-%m-%d").date()
            if fecha_devolucion else None
        )

        prestamo.estado = request.form["estado"]

        if prestamo.estado not in ["Prestado", "Devuelto"]:
            raise ValueError("Estado inválido")

        db.session.commit()
        flash("Préstamo actualizado correctamente.", "success")

    except (ValueError, KeyError):
        db.session.rollback()
        flash("Verifica los datos ingresados.", "danger")

    return redirect(url_for("prestamos.index"))


@prestamos_bp.route("/prestamos/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    prestamo = db.session.get(Prestamo, id)

    if prestamo:
        db.session.delete(prestamo)
        db.session.commit()
        flash("Préstamo eliminado correctamente.", "success")
    else:
        flash("Préstamo no encontrado.", "danger")

    return redirect(url_for("prestamos.index"))
