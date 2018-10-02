from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from productmanager.db import get_db
from productmanager.data import Products

bp = Blueprint('inventory', __name__)
Products = Products()

def get_product():
    product = get_db().execute(
        ' SELECT id, productName, price, quantity, added '
        ' FROM product '
        ' WHERE id = ? ',
        (id,)
    ).fetchone()

    if product is None:
        flash('Product does not exist. Please try again.')
    
    return product

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        ' SELECT id, productName, price, quantity, added'
        ' FROM product'
        ' ORDER BY added ASC'
    ).fetchall()
    print(products)
    return render_template('inventory/index.html', products = products)


@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        productName = request.form['productName']
        quantity = request.form['quantity']
        price = request.form['price']
        error = None

        if not productName:
            error = 'Product name is required.'
        
        if not quantity:
            error = 'Amount of products required.'
        
        if not price:
            error = 'Price is required.'
        
        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'INSERT INTO product (productName, quantity, price)'
                'VALUES (?, ?, ?)', (productName, quantity, price)
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/add.html')

@bp.route('/<int:id>/update', methods=('GET','POST'))
def update(id):
    product = get_product(id)

    if request.method == 'POST':
        productName = request.form['productName']
        quantity = request.form['quantity']
        price = request.form['price']
        error = None

    if not productName:
        error = 'Product name is required.'
    
    if not quantity:
        error = 'Amount of products required.'
    
    if not price:
        error = 'Price is required.'
    
    if error is not None:
        flash(error)

    else:
        db=get_db()
        db.execute(
            ' UPDATE product SET productName = ? quantity = ? price = ? '
            ' WHERE id = ? '
            (productName, quantity, price)
        )
        db.commit()
        return redirect(url_for('inventory.index'))
    return render_template('inventory/update.html', product=product)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    get_product(id)
    db = get_db()
    db.execute( 'DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))

        





