from datetime import date
from app import db


class Prestamo(db.Model):
    __tablename__ = "prestamos"

    id = db.Column(db.Integer, primary_key=True)

    libro_id = db.Column(
        db.Integer,
        db.ForeignKey("libros.id"),
        nullable=False
    )

    lector_id = db.Column(
        db.Integer,
        db.ForeignKey("lectores.id"),
        nullable=False
    )

    fecha_prestamo = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    fecha_devolucion = db.Column(
        db.Date,
        nullable=True
    )

    estado = db.Column(
        db.String(20),
        nullable=False,
        default="Prestado"
    )

    libro = db.relationship("Libro", backref="prestamos")
    lector = db.relationship("Lector", backref="prestamos")
