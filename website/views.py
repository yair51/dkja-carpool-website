from threading import current_thread
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from website.auth import login
from .models import User, Vehicle
from . import db

views = Blueprint('views', __name__)

@views.route("/")
def home():
    vehicles = User.query.all()
    return render_template("arrivals.html", title="Arrivals", vehicles=vehicles, user=current_user)
    #"<p>Hello, World!</p>"

@views.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", user=current_user)

@views.route("/add-vehicle/", methods=['GET', 'POST'])
@views.route("/add-vehicle", methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'POST':
        license_number = request.form.get("license-number")
        print(license_number)
        
        # checks to see if the license plate is registered
        vehicle = Vehicle.query.filter_by(license_number=license_number).first()
        if vehicle:
            flash('License already registered.', category='error')
        else:
            new_vehicle = Vehicle(license_number=license_number, on_campus=False, user_id=current_user.id)
            db.session.add(new_vehicle)
            db.session.commit()

    return render_template("add-vehicle.html", title="Add Vehicle", user=current_user)


@views.route("/profile", methods=['GET', 'POST'])
@views.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id)
    return render_template("profile.html", title="Profile", user=current_user, vehicles=vehicles)