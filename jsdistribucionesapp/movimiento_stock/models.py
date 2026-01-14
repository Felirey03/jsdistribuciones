from datetime import datetime, timezone
from jsdistribucionesapp.app import db


class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey('productos.pid'),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)

    tipo = db.Column(
        db.String(10),
        nullable=False
    )  

    stock_anterior = db.Column(db.Integer, nullable=False)
    stock_nuevo = db.Column(db.Integer, nullable=False)

    motivo = db.Column(db.String(100), nullable=False)

    referencia = db.Column(db.String(100))

    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    producto = db.relationship('Producto', backref='movimientos_stock')
