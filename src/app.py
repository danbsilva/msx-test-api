import os
from flask import Flask
from src import extensions


app = Flask(__name__, static_folder='static', template_folder='docs/templates')
settings = os.path.join(os.path.dirname(__file__), 'settings.py')

def minimal_app():
    app.config.from_pyfile(settings)
    return app


def create_app():
    app = minimal_app()
    extensions.load(app)
    return app
