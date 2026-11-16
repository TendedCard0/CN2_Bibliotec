from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.lector import Lector

lectores_bp = Blueprint('lectores', __name__, url_prefix='/lectores')

@lectores_bp.route('/')
def index():
    lista_lectores = Lector.query.order_by(Lector.id.asc()).all()
    activos = sum(1 for l in lista_lectores if l.activo)
    inactivos = len(lista_lectores) - activos
    mensaje = request.args.get('msg')
    tipo = request.args.get('tipo', 'success')

    return render_template(
        'lectores/index.html',
        lectores=lista_lectores,
        total_activos=activos,
        total_inactivos=inactivos,
        mensaje=mensaje,
        tipo=tipo
    )

@lectores_bp.route('/crear', methods=['POST'])
def crear():
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()

    if not nombre or not email:
        return redirect(url_for('lectores.index', msg='El nombre y correo son obligatorios.', tipo='danger'))

    if Lector.query.filter_by(email=email).first():
        return redirect(url_for('lectores.index', msg='Ese correo ya está registrado.', tipo='warning'))

    nuevo_lector = Lector(nombre=nombre, email=email, telefono=telefono, activo=True)
    db.session.add(nuevo_lector)
    db.session.commit()
    return redirect(url_for('lectores.index', msg='Lector registrado correctamente.', tipo='success'))

@lectores_bp.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    lector = Lector.query.get_or_404(id)
    lector.nombre = request.form.get('nombre', lector.nombre).strip()
    lector.email = request.form.get('email', lector.email).strip()
    lector.telefono = request.form.get('telefono', '').strip()
    lector.activo = 'activo' in request.form

    db.session.commit()
    return redirect(url_for('lectores.index', msg='Lector actualizado correctamente.', tipo='success'))

@lectores_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    lector = Lector.query.get_or_404(id)
    try:
        db.session.delete(lector)
        db.session.commit()
        return redirect(url_for('lectores.index', msg='Lector eliminado.', tipo='success'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('lectores.index', msg='No se puede eliminar porque tiene registros asociados.', tipo='danger'))