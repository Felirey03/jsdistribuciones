from datetime import date
from jsdistribucionesapp.app import db

class Remito(db.Model):
    __tablename__ = "remitos"

    rid = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date, default=date.today)
    direccion_entrega = db.Column(db.String(200))
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(20), default="BORRADOR", nullable=False)


    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('clientes.cid'),
        nullable=False
    )
    

    items = db.relationship(
    'Remito_item',
    backref='remito',
    cascade='all, delete-orphan'
    )

    
    cliente = db.relationship('Cliente')