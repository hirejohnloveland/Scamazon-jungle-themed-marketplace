from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)

    def __init__(self, name, desc, price, image_url):
        self.name = name
        self.desc = desc
        self.price = price
        self.image_url = image_url
