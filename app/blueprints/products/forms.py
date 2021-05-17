from flask.app import Flask
from wtforms import SubmitField
from flask_wtf import FlaskForm


class AddToCartForm(FlaskForm):
    submit = SubmitField()


class CartForm(FlaskForm):
    remove_item = SubmitField()
    clear_cart = SubmitField()
    check_out = SubmitField()

