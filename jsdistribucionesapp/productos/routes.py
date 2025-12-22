from flask import Blueprint, request, redirect, render_template, url_for

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.productos.models import Producto

productos = Blueprint("productos",__name__,template_folder='templates')

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
        producto.nombre = request.get.form('nombre')
        producto.departamento = request.get.form('departamento')
        producto.precio = request.get.form('precio')
        producto.stock = request.get.form('stock')

        db.session.commit()
        return redirect(url_for("productos.index"))
    
    return render_template('productos/editar.html', producto=producto)


    



