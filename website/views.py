from threading import current_thread
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from website.auth import login
from .models import User, Vehicle, Arrival, Child
from . import db, admin

views = Blueprint('views', __name__)

@views.route("/")
def home():
    # queries all of the arrivals
    arrivals = db.session.query(Arrival, User).filter(Arrival.user_id == User.id)
    for arrival in arrivals:
        print(arrival)
    vehicles = User.query.all()
    return render_template("arrivals.html", title="Arrivals", vehicles=vehicles, user=current_user, arrivals=arrivals)
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

@views.route("/scan/<int:user_id>/", methods=['GET', 'POST'])
@views.route("/scan/<int:user_id>", methods=['GET', 'POST'])
def scan(user_id):
    # arrivals = Arrival.query.all()
    # if this route is reached, add a new arrival to the table
    if request:
        # let id and time get set by default
        # set user_id to the value from the route 
        new_arrival = Arrival(user_id=user_id)
        db.session.add(new_arrival)
        db.session.commit()
    # returns to home page after new arrival is logged
    return redirect(url_for("views.home"))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Arrival, db.session))
admin.add_view(ModelView(Child, db.session))