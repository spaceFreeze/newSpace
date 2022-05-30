from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
<<<<<<< HEAD
=======

    with app.app_context():
        db.create_all()

    from . import models
>>>>>>> 8651dd5a29957cc1ea950b3a7efa04ff9a4f9f97

    from . import models
    from .views import main_views, prework_views, hash_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(hash_views.bp)
    return app
