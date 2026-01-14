from flask import Blueprint, request, redirect, render_template, url_for

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.movimiento_stock.models import MovimientoStock
from jsdistribucionesapp.productos.models import Producto

movimiento_stock = Blueprint("movimiento_stock",__name__,template_folder='templates')


@movimiento_stock.route('/producto/<int:producto_id>')
def historial_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    movimientos = (
        MovimientoStock.query
        .filter_by(producto_id=producto_id)
        .order_by(MovimientoStock.fecha.desc())
        .all()
    )

    return render_template(
        'movimiento_stock/historial.html',
        producto=producto,
        movimientos=movimientos
    )


