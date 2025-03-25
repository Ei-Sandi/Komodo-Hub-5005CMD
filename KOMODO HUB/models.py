from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    dob = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(10), default = "student")
    class_id = db.Column(db.Integer)
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.org_id'))

    def __repr__(self):
        return f"<User: {self.username}, Role: {self.role}>"
    
    def get_id(self):
        return self.uid
    
class Organisation(db.Model):
    __tablename__ = "organisation"
    org_id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200), unique=True, nullable = False)
    province = db.Column(db.String(120), nullable = False)
    country = db.Column(db.String(60), default = 'Indonesia')
    logo_data = db.Column(db.LargeBinary)
    logo_type = db.Column(db.Text)
    intro = db.Column(db.Text)
    access_code = db.Column(db.String(10))

    def __repr__(self):
        return f"Reg_Org('{self.org_name})"
    
class Classsroom(db.Model):
    __tablename__ = "classroom"
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable = False)

class module(db.Model):
    __tablename__ = "module"
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(100), nullable = False)

class user_model(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, primary_key=True)

class Messages(db.Model):
    __tablename__ = "chat_logs"
    id = db.Column(db.Integer, primary_key = True)
    Message = db.Column(db.Text)
