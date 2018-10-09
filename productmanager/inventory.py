from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from decimal import Decimal

from productmanager.db import get_db
from productmanager.data import Products
#import pdb; pdb.set_trace()
bp = Blueprint('inventory', __name__)
Products = Products()

def get_product(id):
    product = get_db().execute(
        ' SELECT id, productName, price, quantity, added '
        ' FROM product '
        ' WHERE id = ? ',
        (id,)
    ).fetchone()

    if product is None:
        flash('Product does not exist. Please try again.')
    #Turn product to dictionary
    return dict(product)


def get_value():
    inventory_value = 0
    db = get_db()
    prices = db.execute(
        ' SELECT printf("%.2f", price) AS price, quantity '
        ' FROM product '
    ).fetchall()

    if inventory_value is None:
        inventory_value = 'Error retrieving inventory value.'

    else:
        for item in prices:
            inventory_value = inventory_value + (Decimal(item[0]) * int(item[1]))

    return inventory_value


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        ' SELECT id, productName, printf("%.2f", price) AS price, quantity, added'
        ' FROM product'
        ' ORDER BY added ASC'
    ).fetchall()
    inventory_val = get_value()
    return render_template('inventory/index.html', products = products, inventory_val=inventory_val)



@bp.route('/add', methods=('GET', 'POST'))
@bp.route('/<int:id>/update', methods=('GET','POST'))
def handleProduct(id=[]):
    # Combine Add and Update. If there is a product ID, route it to update
    #else, route it to add
    formTitle = 'Add Product'
    product = ''
    if id:
      product = get_product(id)
      formTitle = 'Edit Product'

    if request.method == 'POST':
        if request.form['button'] == 'Save':
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

            if not id:
                db=get_db()
                db.execute(
                    'INSERT INTO product (productName, quantity, price)'
                    'VALUES (?, ?, ?)', (productName, quantity, price)
                )
                db.commit()
                return redirect(url_for('inventory.index'))

            else:
                db=get_db()
                db.execute(
                    'UPDATE product SET productName = ?, quantity = ?, price = ?'
                    'WHERE id = ?',
                    (productName, quantity, price, id)
                )
                db.commit()
                return redirect(url_for('inventory.index'))


        elif request.form['button'] == 'Back':
            return redirect(url_for('inventory.index'))

    return render_template('inventory/productform.html', product=product, formTitle=formTitle)

@bp.route('/<int:id>/delete', methods=('GET', 'POST',))
def delete(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))

        





