from flask import Blueprint, request, redirect, render_template, url_for

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.productos.models import Producto

productos = Blueprint("productos",__name__,template_folder='templates')

@productos.route('/')
def index():
    productos = Producto.query.all()
    return render_template('productos/index.html', productos=productos)


@productos.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'GET':
        return render_template('productos/agregar.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')

        producto = Producto(
            nombre = nombre,
            precio = float(precio),
            stock = stock,
        )

        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('productos.index'))
    



