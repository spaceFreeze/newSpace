from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# import config     # config 폴더 생성 후 주석 처리

# sqlite 오류 방지
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
    # app.config.from_object(config)    # config 폴더 따로 생성 후 수정
    # 환경변수 APP_CONFIG_FILE에 정의된 파일을 환경 파일로 사용할 것
    # sksk.cmd 파일 수정해야됨
    # set APP_CONFIG_FILE=c:\projects\sksk\config\development.py
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, prework_views, hash_views
    app.register_blueprint(main_views.bp)
    # app.register_blueprint(prework_views.bp)
    app.register_blueprint(hash_views.bp)

    return app
