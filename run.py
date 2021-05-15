from app import create_app, db
from app.blueprints.users.models import User
from app.blueprints.products.models import Product

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product}
