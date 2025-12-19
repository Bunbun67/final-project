from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from routes import register_routes, login_routes, logout_routes, trip_routes
from models import User, db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tripplanner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret-key-change-this'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

register_routes(app,db,bcrypt)
login_routes (app,db)
logout_routes(app)
trip_routes(app)

if __name__ == "__main__":
    app.run(debug=True)


