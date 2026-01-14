from jsdistribucionesapp.app import db

class Remito_item(db.Model):
    __tablename__ = 'remito_items'


    id = db.Column(db.Integer, primary_key=True)
    
    remito_id = db.Column(
        db.Integer,
        db.ForeignKey('remitos.rid'),
        nullable=False
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey('productos.pid'),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto')