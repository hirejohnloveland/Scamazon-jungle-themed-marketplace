from app import create_app, db
from app.blueprints.users.models import User
from app.blueprints.products.models import Product
from app.blueprints.products.db_init import populate_products

app = create_app()

# db_init is the script which initially populates the database with the items


@app.shell_context_processor
def make_shell_context():
    return {'app': create_app, 'db': db, 'User': User, 'Product': Product, 'db_init': populate_products}
