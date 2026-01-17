from jsdistribucionesapp.app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    pid = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    departamento = db.Column(db.String)
    activo = db.Column(db.Boolean, default=True)

    

