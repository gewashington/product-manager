from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from productmanager.db import get_db

bp = Blueprint('inventory', __name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        ' SELECT id, productName, price, quantity'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('/index.html', products=products)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        productName = request.form['productName']
        quantity = request.form['quantity']
        price = request.form['price']

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
                'VALUES (?, ?, ?)'
            )
            db.commit()
            return redirect(url_for('/'))
    return render_template('/add.html')



