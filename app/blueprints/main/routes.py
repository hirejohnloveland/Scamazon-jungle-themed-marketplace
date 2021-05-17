from flask.globals import request
from . import bp as main
from flask import render_template, current_app as app, url_for
from app.blueprints.products.routes import is_empty
from ..products.models import Product


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(
        page, app.config['ITEMS_PER_PAGE'], False)

    next_url = url_for('main.index', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('main.index', page=products.prev_num) \
        if products.has_prev else None
    cart_empty = is_empty()
    return render_template('index.html', products=products.items, next_url=next_url,
                           prev_url=prev_url, cart_empty=cart_empty)
