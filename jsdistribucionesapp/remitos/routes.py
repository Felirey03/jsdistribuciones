from datetime import date, datetime
from collections import defaultdict
from flask import Blueprint, flash, json, request, redirect, render_template, url_for
from sqlalchemy.orm import joinedload

#importamos base de datos y el modelo de la base de datos
from jsdistribucionesapp.app import db
from jsdistribucionesapp.productos.models import Producto
from jsdistribucionesapp.remito_item.models import Remito_item
from jsdistribucionesapp.remitos.models import Remito
from jsdistribucionesapp.clientes.models import Cliente
from jsdistribucionesapp.movimiento_stock.utils import registrar_movimiento_stock



remitos = Blueprint("remitos",__name__,template_folder='templates')


@remitos.route('/')
def index():
    remitos = (
        Remito.query
        .options(joinedload(Remito.cliente))
        .order_by(Remito.rid.desc())
        .all()
    )
    return render_template('remitos/index.html', remitos=remitos)


@remitos.route('/agregar', methods=['GET', 'POST'])
def agregar():
    clientes = Cliente.query.filter_by(activo=True).all()
    productos = Producto.query.all()

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        cliente_id = request.form.get('cliente_id')
        direccion_entrega = request.form.get('direccion_entrega')
        observaciones = request.form.get('observaciones')
        items_raw = request.form.get('items')

        if not cliente_id:
            flash('Debes seleccionar un cliente', 'error')
            return redirect(url_for('remitos.agregar'))

        if not items_raw:
            flash('Debes agregar al menos un producto', 'error')
            return redirect(url_for('remitos.agregar'))

        items = json.loads(items_raw)

        
        acumulado = defaultdict(int)
        for item in items:
            acumulado[int(item['producto_id'])] += int(item['cantidad'])

        
        for producto_id, total in acumulado.items():
            producto = Producto.query.get(producto_id)

            if not producto:
                flash("Producto inexistente", "error")
                return redirect(url_for('remitos.agregar'))

            if total > producto.stock:
                flash(
                    f"No hay stock suficiente de {producto.nombre}. "
                    f"Disponible: {producto.stock}, solicitado: {total}",
                    "error"
                )
                return redirect(url_for('remitos.agregar'))

        
        nuevo_remito = Remito(
            fecha=datetime.strptime(fecha, '%Y-%m-%d') if fecha else None,
            cliente_id=cliente_id,
            direccion_entrega=direccion_entrega,
            observaciones=observaciones,
            estado='BORRADOR'
        )

        db.session.add(nuevo_remito)
        db.session.flush()  

        
        for item in items:
            remito_item = Remito_item(
                remito_id=nuevo_remito.rid,
                producto_id=item['producto_id'],
                cantidad=int(item['cantidad'])
            )
            db.session.add(remito_item)

        db.session.commit()

        flash('Remito creado correctamente', 'success')
        return redirect(url_for('remitos.index'))

    return render_template(
        'remitos/agregar.html',
        clientes=clientes,
        productos=productos
    )


@remitos.route('/<int:id>')
def ver(id):
    remito = (
        Remito.query
        .options(joinedload(Remito.cliente))
        .get_or_404(id)
    )
    return render_template('remitos/ver.html', remito=remito)


@remitos.route('/confirmar/<int:id>', methods=['POST'])
def confirmar(id):
    remito = Remito.query.get_or_404(id)

    
    if remito.estado == 'CONFIRMADO':
        flash('Este remito ya está confirmado', 'warning')
        return redirect(url_for('remitos.ver', id=id))

   
    for item in remito.items:
        producto = item.producto

        if item.cantidad > producto.stock:
            flash(
                f'Stock insuficiente para {producto.nombre}. '
                f'Disponible: {producto.stock}',
                'danger'
            )
            return redirect(url_for('remitos.ver', id=id))

   
    for item in remito.items:
        producto = item.producto

        stock_anterior = producto.stock
        producto.stock -= item.cantidad
        stock_nuevo = producto.stock

        registrar_movimiento_stock(
            producto_id=producto.pid,
            tipo='SALIDA',
            cantidad=item.cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo='Confirmación de remito',
            referencia=f'Remito #{remito.rid}'
        )

  
    remito.estado = 'CONFIRMADO'

   
    db.session.commit()

    flash('Remito confirmado y stock actualizado correctamente', 'success')
    return redirect(url_for('remitos.ver', id=id))


@remitos.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    remito = Remito.query.get_or_404(id)

    if remito.estado == 'CONFIRMADO':
        flash('No se puede eliminar un remito confirmado', 'error')
        return redirect(url_for('remitos.ver', id=id))

    db.session.delete(remito)
    db.session.commit()

    flash('Remito eliminado', 'success')
    return redirect(url_for('remitos.index'))


@remitos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    remito = Remito.query.get_or_404(id)

    if remito.estado == 'CONFIRMADO':
        flash('Este remito está confirmado y no puede editarse.', 'warning')
        return redirect(url_for('remitos.ver', id=id))

    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        if fecha_str:
            remito.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
        remito.direccion_entrega = request.form.get('direccion_entrega')
        remito.observaciones = request.form.get('observaciones')

        items_json = request.form.get('items_json')
        if not items_json:
            flash('El remito debe tener al menos un producto.', 'danger')
            return redirect(url_for('remitos.editar', id=id))

        items_nuevos = json.loads(items_json)

        items_actuales = {
            item.producto_id: item
            for item in remito.items
        }

        productos_ids_nuevos = set()

        for item in items_nuevos:
            producto_id = int(item['producto_id'])
            cantidad = int(item['cantidad'])
            productos_ids_nuevos.add(producto_id)

            if producto_id in items_actuales:
            
                items_actuales[producto_id].cantidad = cantidad
            else:
                
                nuevo_item = Remito_item(
                    remito_id=remito.rid,
                    producto_id=producto_id,
                    cantidad=cantidad
                )
                db.session.add(nuevo_item)

       
        for producto_id, item in items_actuales.items():
            if producto_id not in productos_ids_nuevos:
                db.session.delete(item)

        db.session.commit()

        flash('Remito actualizado correctamente.', 'success')
        return redirect(url_for('remitos.ver', id=id))

    
    productos = Producto.query.all()

    items_json = [
        {
            "producto_id": item.producto_id,
            "cantidad": item.cantidad,
            "nombre": item.producto.nombre
        }
        for item in remito.items
    ]

    return render_template(
        'remitos/editar.html',
        remito=remito,
        productos=productos,
        items_json=items_json
    )

@remitos.route('/<int:id>/print')
def print(id):
    remito = Remito.query.get_or_404(id)
    return render_template('remitos/print.html', remito=remito)


    
        


