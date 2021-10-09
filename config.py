import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # General Flask config #
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    
    # WTForms CSRF Config #
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("Secret Key Not Provided, Please add to .env file")

    # SQL Alchemy database config #
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    
    # Flask Mail Config #
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Stripe Pay config #
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    # Pagination Config #
    ITEMS_PER_PAGE = 8
