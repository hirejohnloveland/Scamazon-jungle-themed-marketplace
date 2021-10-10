# Scamazon-jungle-themed-marketplace

Scamazon "Jungle Themed Marketplace" is a full stack Flask e-commerce application based on the fake products of Obvious Plant.  It features an ElephantSQL
database and is designed with the Bootstrap UI framework.  

## Features:

### Flask 
Blueprinted Flask application with app factory pattern.
Fully functional user authentication blueprint allows users to register, authenticate, and provides password reset e-mails with JWS token authentication.
DB_init.py file works with Flask Migrate to build the database for new deployments
SQLAlchemy ORM wrapper for database layer
Flask-Login authenticates users and redirects to the login page if they try to buy something prior to login, then the item is added to the cart and the user redirected to the product page
