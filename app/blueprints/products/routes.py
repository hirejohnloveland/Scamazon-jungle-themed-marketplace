from app.blueprints.products.forms import AddToCartForm
from app import db
from flask.helpers import url_for
from werkzeug.utils import redirect
from . import bp as products
from flask import render_template, flash
from .models import Product, Cart
from flask_login import current_user, login_required
from .forms import AddToCartForm, CartForm


@products.route('/products/<int:product_id>')
def show_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    cart_empty = is_empty()
    return render_template('product_view.html', product=product, form=form, cart_empty=cart_empty)


@products.route('/products/add/<int:product_id>/<int:qty>', methods=['POST'])
@login_required
def add_to_cart(product_id, qty):
    form = AddToCartForm()
    if form.validate_on_submit():
        user_id = current_user.id
        cart = Cart(product_id, qty, user_id)
        db.session.add(cart)
        db.session.commit()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@ products.route('/cart')
@ login_required
def show_cart():
    form = CartForm()
    items = db.session.query(Cart, Product).join(
        Product).filter(Cart.user_id == current_user.id)
    sum = 0
    for item in items:
        sum = sum + item[1].price
    print(sum)
    cart_empty = is_empty()
    return render_template('shopping_cart.html', items=items, form=form, sum=sum, cart_empty=cart_empty)


@ products.route('/cart/remove/<int:cart_id>', methods=['POST'])
@ login_required
def remove_items(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    print(cart_item)
    if cart_item.user_id != current_user.id:
        flash("You cannot update another user's cart", 'danger')
    form = CartForm()
    if form.validate_on_submit():
        db.session.delete(cart_item)
        db.session.commit()
        return redirect(url_for('products.show_cart'))
    return redirect(url_for('main.index'))


@ products.route('/cart/remove/clear', methods=['POST'])
@ login_required
def clear_cart():
    form = CartForm()
    if form.validate_on_submit():
        total_cart = Cart.query.filter(Cart.user_id == current_user.id)
        for items in total_cart:
            db.session.delete(items)
            db.session.commit()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@ products.route('/cart/remove/clear', methods=['POST'])
@ login_required
def check_out():
    clear_cart()
    return redirect(url_for('main.index'))


def is_empty():
    if not current_user.is_authenticated:
        return True
    items = db.session.query(Cart, Product).join(
        Product).filter(Cart.user_id == current_user.id)
    if items.count() == 0:
        return True
    else:
        return False
