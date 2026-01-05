from jsdistribucionesapp.app import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    cid = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String)
    telefono = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    cuit = db.Column(db.String)
    activo = db.Column(db.Boolean, default=True)

