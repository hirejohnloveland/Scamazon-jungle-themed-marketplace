from app.blueprints.products.forms import AddToCartForm
from app import db
from flask import current_app as app
from flask.helpers import url_for
from werkzeug.utils import redirect
from . import bp as products
from flask import render_template, flash
from .models import Product, Cart
from flask_login import current_user, login_required
from .forms import AddToCartForm, CartForm
import stripe

##################################################################
############### PRODUCT INFORMATION PAGE  ########################
##################################################################


@products.route('/products/<int:product_id>')
def show_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    cart_empty = is_empty()
    return render_template('product_view.html', product=product, form=form, cart_empty=cart_empty)

##################################################################
############### ADD TO CART ######################################
##################################################################

# Page is not displayed, this route adds an item to the cart and redirects to the index


@products.route('/products/add/<int:product_id>/<int:qty>', methods=['POST'])
@login_required
def add_to_cart(product_id, qty):
    # if not current_user.is_authenticated:
    #     return redirect(url_for('users.login'))
    form = AddToCartForm()
    if form.validate_on_submit():
        user_id = current_user.id
        cart = Cart(product_id, qty, user_id)
        db.session.add(cart)
        db.session.commit()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))

##################################################################
############### REMOVE FROM CART #################################
##################################################################

# Page is not displayed, this route removes an item from the cart and redirects to the cart page


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

##################################################################
############### SHOPPING CART PAGE################################
##################################################################


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

##################################################################
############### CLEAR CART #######################################
##################################################################

# Page is not displayed, this route clears the cart and redirects to the index


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

##################################################################
############### CHECKOUT #########################################
##################################################################

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@ products.route('/cart/checkout', methods=['POST'])
@ login_required
def check_out():
    items = db.session.query(Cart, Product).join(
        Product).filter(Cart.user_id == current_user.id)
    cart_items = []
    for item in items:
        cart_items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': item[1].name,
            },
            'unit_amount': int(item[1].price*100),
        },
        'quantity': 1,
        }
        )
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=cart_items,
        mode='payment',
        success_url=url_for('products.checkout_success',_external=True),
        cancel_url=url_for('products.show_cart', _external=True),
    )

    return redirect(session.url, code=303)

##################################################################
############### CHECKOUT SUCCESS #################################
##################################################################
@ products.route('/cart/checkout/success', methods=['GET'])
@ login_required
def checkout_success():
    total_cart = Cart.query.filter(Cart.user_id == current_user.id)
    for items in total_cart:
        db.session.delete(items)
        db.session.commit()
    cart_empty = is_empty()
    return render_template('success.html',cart_empty=cart_empty)

##################################################################
############### HELPER FUNCTIONS #################################
##################################################################

# Check if the cart is empty to tell the nav bar which cart icon to display


def is_empty():
    if not current_user.is_authenticated:
        return True
    items = db.session.query(Cart, Product).join(
        Product).filter(Cart.user_id == current_user.id)
    if items.count() == 0:
        return True
    else:
        return False
