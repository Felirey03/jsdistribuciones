from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/jsdistribuciones.db'
    app.config['SECRET_KEY'] = '1234'

    from apscheduler.schedulers.background import BackgroundScheduler
    from jsdistribucionesapp.backup import backup_db

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        backup_db,
        trigger="interval",
        hours=6,      # cada 6 horas
        id="backup_db"
    )
    scheduler.start()

    db.init_app(app)

    from jsdistribucionesapp.core.routes import core
    from jsdistribucionesapp.clientes.routes import clientes
    from jsdistribucionesapp.productos.routes import productos
    from jsdistribucionesapp.remitos.routes import remitos
    from jsdistribucionesapp.movimiento_stock.routes import movimiento_stock

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(clientes, url_prefix='/clientes')
    app.register_blueprint(productos, url_prefix='/productos')
    app.register_blueprint(remitos, url_prefix='/remitos')
    app.register_blueprint(movimiento_stock, url_prefix='/movimiento_stock')
    


    migrate = Migrate(app,db)

    return app