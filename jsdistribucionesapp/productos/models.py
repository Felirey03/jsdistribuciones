from jsdistribucionesapp.app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    pid = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.String, default=0)

