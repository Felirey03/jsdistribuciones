from flask import Blueprint, request, redirect, render_template, url_for

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.clientes.models import Cliente

clientes = Blueprint("clientes",__name__,template_folder='templates')

@clientes.route('/')
def index():
    clientes = Cliente.query.order_by(Cliente.nombre.asc()).all()
    return render_template('clientes/index.html', clientes=clientes)

@clientes.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'GET':
        return render_template('clientes/agregar.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        cuit = request.form.get('cuit')
        activo = True if request.form.get("activo") == "on" else False


        nuevo_cliente = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono = telefono,
            email=email,
            cuit=cuit,
            activo=activo,
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

        return redirect(url_for('clientes.index'))
    
@clientes.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre = request.form.get('nombre')
        cliente.direccion = request.form.get('direccion')
        cliente.telefono = request.form.get('telefono')
        cliente.email = request.form.get('email')
        cliente.cuit = request.form.get('cuit')
        cliente.activo = request.form.get('activo') is not None


        db.session.commit()
        return redirect(url_for("clientes.index"))
    
    return render_template('clientes/editar.html', cliente=cliente)


@clientes.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for('clientes.index'))

