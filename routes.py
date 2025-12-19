from flask import request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from models import db, User, Trip, Country, Expense
from schemas import user_schema, trip_schema, country_schema, expense_schema
from datetime import datetime


#authorization routes
def register_routes(app, db, bcrypt):
    @app.route('/')
    def home():
        return redirect(url_for('register')) 

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'password': request.form['password']
            }    
            user_schema.load(data)
            if User.query.filter_by(email=data['email']).first():
                    flash('Email already taken')
                    return render_template('register.html')
            
            password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(name=data['name'], email=data['email'], password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created')

            return redirect(url_for('login'))
        return render_template('register.html')
    
#login routes
def login_routes(app, bcrypt):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')

            # is there a user with this username?
            user = User.query.filter(User.name == name).first()

            if not user or not bcrypt.check_password_hash(user.password_hash, password):
                flash("Invalid username or password")
                return redirect(url_for('login'))
            
            login_user(user)
            return redirect(url_for('index'))
        

#log out route
def logout_routes(app):  
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

#trip routes
def trip_routes(app):
    @app.route('/index')
    @login_required
    def index():
        trips = Trip.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', trips=trips)
    
    @app.route('/trip/create', methods=['GET', 'POST'])
    @login_required
    def create_trip():
        if request.method == 'POST':
            data = {
                'name': request.form['name'],
                'start_date': request.form.get('start_date') or None,
                'end_date': request.form.get('end_date') or None
            }
            
            trip_schema.load(data)

            start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date() 

            trip = Trip(
                name=data['name'],
                start_date=start_date,
                end_date=end_date,
                user_id=current_user.id
            )

            db.session.add(trip)
            db.session.commit()
            return redirect(url_for('trip_details', trip_id=trip.id))

        return render_template('create_trip.html')
    
    #match only URLs that have an integer in the trip id dynamic segment
    @app.route('/trip/<int:trip_id>')
    @login_required
    def trip_details(trip_id):
        #if not found raises http 404 not found error
        trip=Trip.query.get_or_404(trip_id)
        if trip.user_id != current_user.id:
            flash('Unauthorized')
            return redirect(url_for('index'))
        return render_template('trip_detail.html', trip=trip)
    
    @app.route('/trip/<int:trip_id>/country/add', methods=['POST'])
    @login_required
    def add_country(trip_id):
        trip=Trip.query.get_or_404(trip_id)
        if trip.user_id != current_user.id:
            flash('Unauthorized')
            return redirect(url_for('index'))
        
        data = {'name': request.form['name'], 'budget':float(request.form.get('budget', 0))}
        country_schema.load(data)

        country = Country(name=data['name'], budget=data['budget'], trip_id=trip.id)
        db.session.add(country)
        db.session.commit()
        flash('Country added')
        return redirect(url_for('trip_details', trip_id=trip_id))
    
    @app.route('/trip/<int:trip_id>/expense/add', methods=['POST'])
    @login_required
    def add_expenses(country_id):
        country = Country.query.get_or_404(country_id)
        if country.trip.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('index'))
        
        data = {'description': request.form['description'], 'amount': float(request.form['amount'])}
        expense_schema.load(data)

        expense = Expense(description=data['description'], amount=data['amount'], country_id=country.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added')
        return redirect(url_for('trip_details', trip_id=country.trip.id))

 
