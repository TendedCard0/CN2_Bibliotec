from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.libro import Libro

libros_bp = Blueprint('libros', __name__, url_prefix='/libros')

@libros_bp.route('/')
def index():
    libros = Libro.query.order_by(Libro.id.desc()).all()
    return render_template('libros/index.html', libros=libros)

@libros_bp.route('/crear', methods=['POST'])
def crear():
    titulo = request.form.get('titulo', '').strip()
    autor = request.form.get('autor', '').strip()
    isbn = request.form.get('isbn', '').strip()
    editorial = request.form.get('editorial', '').strip()
    anio = request.form.get('anio_publicacion', '').strip()
    disponibles = int(request.form.get('disponibles') or 1)

    existente = Libro.query.filter_by(isbn=isbn).first()
    if existente:
        flash('Ya existe un libro registrado con ese ISBN.', 'danger')
        return redirect(url_for('libros.index'))

    nuevo_libro = Libro(
        titulo=titulo,
        autor=autor,
        isbn=isbn,
        editorial=editorial,
        anio_publicacion=int(anio) if anio else None,
        disponibles=disponibles
    )
    db.session.add(nuevo_libro)
    db.session.commit()
    flash('Libro registrado correctamente.', 'success')
    return redirect(url_for('libros.index'))

@libros_bp.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    libro = Libro.query.get_or_404(id)
    nuevo_isbn = request.form.get('isbn', '').strip()

    isbn_duplicado = Libro.query.filter(Libro.isbn == nuevo_isbn, Libro.id != id).first()
    if isbn_duplicado:
        flash('El ISBN ya pertenece a otro libro.', 'danger')
        return redirect(url_for('libros.index'))

    libro.titulo = request.form.get('titulo', '').strip()
    libro.autor = request.form.get('autor', '').strip()
    libro.isbn = nuevo_isbn
    libro.editorial = request.form.get('editorial', '').strip()
    anio = request.form.get('anio_publicacion', '').strip()
    libro.anio_publicacion = int(anio) if anio else None
    libro.disponibles = int(request.form.get('disponibles') or 1)

    db.session.commit()
    flash('Libro actualizado correctamente.', 'info')
    return redirect(url_for('libros.index'))

@libros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado correctamente.', 'warning')
    return redirect(url_for('libros.index'))