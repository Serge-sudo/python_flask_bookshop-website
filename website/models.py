from . import db
from flask_login import UserMixin


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(2000))
    img_src = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    data = db.Column(db.String(1000))
    type_ = db.Column(db.String(1000))
