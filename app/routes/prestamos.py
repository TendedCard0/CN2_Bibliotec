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

    libros_disponibles = [
        libro for libro in libros if libro.disponibles > 0
    ]

    lectores_activos = [
        lector for lector in lectores if lector.activo
    ]

    return render_template(
        "prestamos/index.html",
        prestamos=prestamos,
        libros=libros,
        lectores=lectores,
        libros_disponibles=libros_disponibles,
        lectores_activos=lectores_activos
    )


@prestamos_bp.route("/prestamos/registrar", methods=["POST"])
def registrar():
    try:
        libro_id = int(request.form.get("libro_id", ""))
        lector_id = int(request.form.get("lector_id", ""))

        fecha_prestamo = datetime.strptime(
            request.form.get("fecha_prestamo", ""),
            "%Y-%m-%d"
        ).date()

        libro = db.session.get(Libro, libro_id)
        lector = db.session.get(Lector, lector_id)

        if not libro or not lector:
            raise ValueError("Selecciona un libro y un lector válidos.")

        if not lector.activo:
            raise ValueError("El lector seleccionado no está activo.")

        if libro.disponibles <= 0:
            raise ValueError("El libro seleccionado no tiene ejemplares disponibles.")

        prestamo = Prestamo(
            libro_id=libro.id,
            lector_id=lector.id,
            fecha_prestamo=fecha_prestamo,
            estado="Prestado"
        )

        libro.disponibles -= 1

        db.session.add(prestamo)
        db.session.commit()

        flash("Préstamo registrado correctamente.", "success")

    except (ValueError, TypeError):
        db.session.rollback()
        flash("No se pudo registrar el préstamo. Verifica los datos y la disponibilidad.", "danger")

    return redirect(url_for("prestamos.index"))


@prestamos_bp.route("/prestamos/editar/<int:id>", methods=["POST"])
def editar(id):
    prestamo = db.session.get(Prestamo, id)

    if not prestamo:
        flash("Préstamo no encontrado.", "danger")
        return redirect(url_for("prestamos.index"))

    try:
        libro_id = int(request.form.get("libro_id", ""))
        lector_id = int(request.form.get("lector_id", ""))

        libro_nuevo = db.session.get(Libro, libro_id)
        lector_nuevo = db.session.get(Lector, lector_id)

        if not libro_nuevo or not lector_nuevo:
            raise ValueError("Selecciona un libro y un lector válidos.")

        fecha_prestamo = datetime.strptime(
            request.form.get("fecha_prestamo", ""),
            "%Y-%m-%d"
        ).date()

        estado_nuevo = request.form.get("estado", "")

        if estado_nuevo not in ("Prestado", "Devuelto"):
            raise ValueError("El estado seleccionado no es válido.")

        fecha_devolucion_texto = request.form.get("fecha_devolucion", "")

        if estado_nuevo == "Devuelto":
            if not fecha_devolucion_texto:
                raise ValueError("Indica la fecha de devolución.")

            fecha_devolucion = datetime.strptime(
                fecha_devolucion_texto,
                "%Y-%m-%d"
            ).date()

            if fecha_devolucion < fecha_prestamo:
                raise ValueError("La fecha de devolución no puede ser anterior al préstamo.")
        else:
            fecha_devolucion = None

        libro_anterior = prestamo.libro
        estado_anterior = prestamo.estado

        cambio_libro = libro_anterior.id != libro_nuevo.id

        if estado_anterior == "Prestado":
            if cambio_libro or estado_nuevo == "Devuelto":
                libro_anterior.disponibles += 1

        if estado_nuevo == "Prestado":
            if estado_anterior == "Devuelto" or cambio_libro:
                if libro_nuevo.disponibles <= 0:
                    raise ValueError("El nuevo libro no tiene ejemplares disponibles.")

                libro_nuevo.disponibles -= 1

        prestamo.libro_id = libro_nuevo.id
        prestamo.lector_id = lector_nuevo.id
        prestamo.fecha_prestamo = fecha_prestamo
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.estado = estado_nuevo

        db.session.commit()

        flash("Préstamo actualizado correctamente.", "success")

    except (ValueError, TypeError) as error:
        db.session.rollback()
        flash(f"Error al actualizar: {error}", "danger")

    return redirect(url_for("prestamos.index"))


@prestamos_bp.route("/prestamos/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    prestamo = db.session.get(Prestamo, id)

    if not prestamo:
        flash("Préstamo no encontrado.", "danger")
        return redirect(url_for("prestamos.index"))

    try:
        if prestamo.estado == "Prestado":
            prestamo.libro.disponibles += 1

        db.session.delete(prestamo)
        db.session.commit()

        flash("Préstamo eliminado correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("Ocurrió un error al eliminar el préstamo.", "danger")

    return redirect(url_for("prestamos.index"))
