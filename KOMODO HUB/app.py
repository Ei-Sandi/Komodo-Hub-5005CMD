from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, join_room, leave_room, send

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///KomodoHub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'

    #for sessions
    app.secret_key = 'KOMODO'

    #for database
    db.init_app(app)

    #for login authentication
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User, Organisation, Messages
    
    with app.app_context():
        db.create_all()
        
    #how login manager loads user
    @login_manager.user_loader
    def load_user(username):
        return User.query.get(username)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("home"))
    
    #to hash passwords, users
    bcrypt = Bcrypt(app)

    from routes import all_routes,register_routes, login_routes, restricted_routes

    all_routes(app)
    register_routes(app,db,bcrypt)
    login_routes(app, bcrypt)
    restricted_routes(app)

    migrate = Migrate(app,db)

    return app
