from threading import current_thread
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from website.auth import login
from .models import User, Vehicle, Arrival, Child
from . import db, admin
from sqlalchemy import func

views = Blueprint('views', __name__)

@views.route("/")
def home():
    # queries all of the arrivals
    
    # subquery = (db.session.query(Arrival, Child, User, func.rank().over(order_by=Arrival.time.desc(),
    # partition_by=Arrival.user_id).label('time_rnk'), func.rank().over(order_by=Child.grade,
    # partition_by=Arrival.user_id).label('grade_rnk'))).filter(Arrival.user_id == Child.user_id, Arrival.user_id == User.id).subquery()
    #children = db.session.query(User, Child).filter(User.id == Child.user_id)
    # this creates the arrival query by showing only 1 arrival per family
    subquery = (db.session.query(Arrival, Child, User, func.rank().over(order_by=Arrival.time.desc(),
    partition_by=Arrival.user_id).label('time_rnk'), func.rank().over(order_by=Child.grade.desc(), partition_by=Arrival.user_id).label('grade_rnk'))).filter(Arrival.user_id == Child.user_id, Arrival.user_id == User.id).order_by(Arrival.time.desc()).subquery()
    arrivals = db.session.query(subquery).filter(
    subquery.c.time_rnk==1)
    # for arrival in arrivals:
    #     print(arrival)
    # for child in children:
    #     print(child)
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
    # queries the user's children and the user, ordered by grade
    children = db.session.query(User, Child).filter(User.id == current_user.id, User.id == Child.user_id).order_by(Child.grade)
    for child in children:
        print(child)
    vehicles = Vehicle.query.filter_by(user_id=current_user.id)
    return render_template("profile.html", title="Profile", user=current_user, vehicles=vehicles, children=children)

@views.route("/scan/<int:user_id>/", methods=['GET', 'POST'])
@views.route("/scan/<int:user_id>", methods=['GET', 'POST'])
@login_required
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