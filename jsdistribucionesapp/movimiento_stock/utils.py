from jsdistribucionesapp.app import db
from jsdistribucionesapp.movimiento_stock.models import MovimientoStock

def registrar_movimiento_stock(
    producto_id,
    tipo,
    cantidad,
    stock_anterior,
    stock_nuevo,
    motivo=None,
    referencia=None
):
    movimiento = MovimientoStock(
        producto_id=producto_id,
        tipo=tipo,
        cantidad=cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=stock_nuevo,
        motivo=motivo,
        referencia=referencia
    )

    db.session.add(movimiento)

