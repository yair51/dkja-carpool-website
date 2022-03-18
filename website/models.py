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

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.String(20))
    on_campus = db.Column(db.Boolean)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

class Arrival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    grade = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    children = db.relationship('Child', backref='parent')
    arrivals = db.relationship('Arrival', backref='parent')
    vehicles = db.relationship('Vehicle', backref='parent')