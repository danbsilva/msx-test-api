from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
    app.db = db

    with app.app_context():
        inspector = inspect(db.engine)
        if 'automations' not in inspector.get_table_names():
            db.create_all()
