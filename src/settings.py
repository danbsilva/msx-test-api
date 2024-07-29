import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# FLASK APP
FLASK_DEBUG = 0 if os.getenv("FLASK_DEBUG") == "False" else 1
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_APP = os.getenv("FLASK_APP")
APP_NAME = os.getenv("APP_NAME")
APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))


# DB
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# SECRET KEY
SECRET_KEY = os.getenv("SECRET_KEY")


# EXTENSIONS
EXTENSIONS = [
    'src.routes:init_app',
    'src.extensions.flask_jwt:init_app',
    'src.extensions.flask_sqlalchemy:init_app',
    'src.extensions.flask_marshmallow:init_app',
]
