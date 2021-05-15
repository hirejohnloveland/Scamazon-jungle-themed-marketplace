from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    login.login_view = 'users.login'
    login.login_message = 'danger'
    with app.app_context():
        from app.blueprints.users import bp as users
        app.register_blueprint(users)

        from app.blueprints.main import bp as main
        app.register_blueprint(main)

        from app.blueprints.products import bp as main
        app.register_blueprint(main)
    return app
