from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    vehicle = db.relationship('Vehicle', backref='user')

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.String(20))
    on_campus = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
