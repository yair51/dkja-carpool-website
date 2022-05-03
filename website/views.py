from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from website.auth import login
from .models import User, Vehicle, Arrival, Child, Parent
from . import db, admin
from sqlalchemy import func, join

views = Blueprint('views', __name__)

@views.route("/")
def home():
    # queries all of the arrivals
    
    # subquery = (db.session.query(Arrival, Child, User, func.rank().over(order_by=Arrival.time.desc(),
    # partition_by=Arrival.parent_id).label('time_rnk'), func.rank().over(order_by=Child.grade,
    # partition_by=Arrival.parent_id).label('grade_rnk'))).filter(Arrival.parent_id == Child.parent_id, Arrival.parent_id == User.id).subquery()
    #children = db.session.query(User, Child).filter(User.id == Child.parent_id)
    # this creates the arrival query by showing only 1 arrival per family
    subquery = (db.session.query(Arrival, Child, Parent, func.rank().over(order_by=Arrival.time.desc(),
    partition_by=Arrival.parent_id).label('time_rnk'),
     func.rank().over(order_by=Child.grade.desc(),
      partition_by=Arrival.parent_id).label('grade_rnk'))).filter(Arrival.parent_id == Child.parent_id,
       Arrival.parent_id == Parent.id).order_by(Arrival.time.desc()).subquery()
    arrivals = db.session.query(subquery).filter(
    subquery.c.time_rnk==1)
    for arrival in arrivals:
        print(arrival)
    # for child in children:
    #     print(child)
    vehicles = User.query.all()
    return render_template("arrivals.html", title="Arrivals", vehicles=vehicles, user=current_user, arrivals=arrivals)
    #"<p>Hello, World!</p>"

@views.route("/parents")
def parents():
        names = Parent.query.all()
        return render_template("parents.html", title="Parents",user=current_user, names=names)


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
            new_vehicle = Vehicle(license_number=license_number, on_campus=False, parent_id=current_user.id)
            db.session.add(new_vehicle)
            db.session.commit()

    return render_template("add-vehicle.html", title="Add Vehicle", user=current_user)


@views.route("/profile/<int:parent_id>/", methods=['GET', 'POST'])
@views.route("/profile/<int:parent_id>", methods=['GET', 'POST'])
@login_required
def profile(parent_id):
    # queries the parent's children and the parent, ordered by grade
    children = db.session.query(Parent, Child).filter(Parent.id == parent_id, Parent.id == Child.parent_id).order_by(Child.grade)
    for child in children:
        print(child)
    vehicles = Vehicle.query.filter_by(parent_id=current_user.id)
    # parent = db.session.query(Parent).filter(Parent.id == parent_id)
    # print(parent.first_name)
    # for parent in parents:
    #     print(parent.first_name)
    return render_template("profile.html", title="Profile", user=current_user, vehicles=vehicles, children=children)

@views.route("/scan", methods=['GET', 'POST'])
@views.route("/scan/", methods=['GET', 'POST'])
@views.route("/scan/<int:parent_id>/", methods=['GET', 'POST'])
@views.route("/scan/<int:parent_id>", methods=['GET', 'POST'])
def scan(parent_id=0):
    # arrivals = Arrival.query.all()
    # if this route is reached and  add a new arrival to the table
    if request:
        # if parent_id equals zero, check the license number
        if parent_id == 0:
            # looks for parameter value for license
            license_number = request.args.get('license')
            print(license_number)
            # if a value exists, search for it in database
            if license_number:
                vehicle = Vehicle.query.filter_by(license_number=license_number).first()
                if not vehicle:
                    return redirect(url_for("views.home"))
                else:
                    print(vehicle)
                    parent_id = vehicle.parent_id
            # if no license in URL, return to home screen
            else:
                return redirect(url_for("views.home"))
        # let id and time get set by default
        # set parent_id to the value from the route 
        new_arrival = Arrival(parent_id=parent_id)
        db.session.add(new_arrival)
        db.session.commit()
    # returns to home page after new arrival is logged
    return redirect(url_for("views.home"))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Arrival, db.session))
admin.add_view(ModelView(Child, db.session))
admin.add_view(ModelView(Parent, db.session))