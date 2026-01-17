from flask import Blueprint, request, redirect, render_template, url_for, flash

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.productos.models import Producto

productos = Blueprint("productos",__name__,template_folder='templates')
DEPARTAMENTOS = ["yerba", "infusiones", "almacen", "bebidas"]


@productos.route('/')
def index():
    productos = Producto.query.order_by(Producto.nombre.asc()).all()
    return render_template('productos/index.html', productos=productos)


@productos.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'GET':
        return render_template('productos/agregar.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        departamento = request.form.get('departamento')

        producto = Producto(
            nombre = nombre,
            departamento = departamento,
            precio = float(precio),
            stock = stock,
        )

        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('productos.index'))
    

@productos.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.departamento = request.form.get('departamento')
        producto.precio = request.form.get('precio')
        producto.stock = request.form.get('stock')
        producto.activo = True if request.form.get('activo') == 'on' else False

    
        flash('Producto actualizado correctamente', 'success')
    
        
        db.session.commit()
        return redirect(url_for("productos.index"))
    
    return render_template('productos/editar.html', producto=producto, departamentos=DEPARTAMENTOS)



@productos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    producto = Producto.query.get_or_404(id)

    if producto.movimientos_stock:
        producto.activo = False
        db.session.commit()

        flash(
            'El producto tiene movimientos de stock y fue desactivado '
            '(no puede eliminarse).',
            'info'
        )
        return redirect(url_for('productos.index'))

    db.session.delete(producto)
    db.session.commit()

    flash('Producto eliminado definitivamente', 'success')
    return redirect(url_for('productos.index'))   


@productos.route('/cambiar-precio', methods=['POST'])
def cambiar_precio():
    ids = request.form.get('ids')
    nuevo_precio = request.form.get('precio')

    if not ids or not nuevo_precio:
        return redirect(url_for('productos.index'))

    ids_lista = ids.split(',')

    productos = Producto.query.filter(Producto.pid.in_(ids_lista)).all()

    for producto in productos:
        producto.precio = nuevo_precio

    db.session.commit()

    return redirect(url_for('productos.index'))




