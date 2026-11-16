from app import db

class Lector(db.Model):
    __tablename__ = 'lectores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Lector {self.nombre}>'