from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Product, Order
from ..forms import ProductForm
from .. import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/list')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product.add_product'))
    return render_template('add_product.html', form=form)


@product_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def product_detail(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        total_price = quantity * product.price
        order = Order(product_id=product.id, quantity=quantity, total_price=total_price)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('product.product_list'))
    return render_template('order.html', product=product)
