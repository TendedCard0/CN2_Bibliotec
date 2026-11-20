from app import db

class Libro(db.Model):
    __tablename__ = 'libros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(30), unique=True, nullable=False)
    editorial = db.Column(db.String(100), nullable=True)
    anio_publicacion = db.Column(db.Integer, nullable=True)
    disponibles = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Libro {self.titulo}>'