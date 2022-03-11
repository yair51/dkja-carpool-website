from sqlalchemy import false
from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    vehicle = db.relationship('Vehicle', backref='user')
    arrivals = db.relationship('Arrival', backref='user')
    children = db.relationship('Child', backref='user')

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.String(20))
    on_campus = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Arrival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    grade = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
