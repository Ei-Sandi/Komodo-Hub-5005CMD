from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    dob = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    code = db.Column(db.String(10))
    role = db.Column(db.String(10), default = "student")

    def __repr__(self):
        return f"<User: {self.username}, Role: {self.role}>"
    
    def get_id(self):
        return self.uid
    
class Organisation(db.Model):
    __tablename__ = "organisation"
    org_name = db.Column(db.String(200), primary_key=True)
    province = db.Column(db.String(120))
    country = db.Column(db.String(60))
    logo_img = db.Column(db.Text)
    logo_name = db.Column(db.Text)
    logo_type = db.Column(db.Text)
    intro = db.Column(db.Text)

    def __repr__(self):
        return f"Reg_Org('{self.org_name})"

class Messages(db.Model):
    __tablename__ = "chat_logs"
    id = db.Column(db.Integer, primary_key = True)
    Message = db.Column(db.Text)
