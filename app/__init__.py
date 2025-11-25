# app/__init__.py

from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change_this_secret_key'  # change to anything random

    app.register_blueprint(main)

    return app
