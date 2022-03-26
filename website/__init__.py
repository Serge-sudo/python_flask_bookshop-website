from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy.sql import text

db = SQLAlchemy()
DB_NAME = "base.db"


def create_website():
    web = Flask(__name__)
    web.config["SECRET_KEY"] = "Hello World!"
    web.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(web)

    from .views import views
    from .auth import auth

    web.register_blueprint(views, url_prefix="/")
    web.register_blueprint(auth, url_prefix="/")

    from .models import products

    create_database(web)

    return web


def create_database(web):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=web)
        print("created new database")
