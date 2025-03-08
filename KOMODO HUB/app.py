from flask import Flask, render_template, url_for, request, redirect, flash
from flask import Flask, render_template, url_for, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
import warnings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'KOMODO'

db=SQLAlchemy(app)



class Reg_Ind(db.Model):
    __tablename__ = "Individual"
    Username = db.Column(db.String(100), primary_key=True)
    Email = db.Column(db.String(120), unique=True)
    First_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50))
    DOB = db.Column(db.String(10))
    Password = db.Column(db.String(100))
    Code = db.Column(db.String(10))

    def __repr__(self):
        return f"{self.Username}, {self.Email}, {self.Password}"


class Reg_Org(db.Model):
    __tablename__ = "Organisation"
    Org_Name = db.Column(db.String(200), primary_key=True)
    Province = db.Column(db.String(120))
    Country = db.Column(db.String(60))
    Logo_Img = db.Column(db.Text)
    Logo_Name = db.Column(db.Text)
    Logo_Mime = db.Column(db.Text)
    Info = db.Column(db.Text)

    def __repr__(self):
        return f"Reg_Org('{self.Org_Name})"
    


with app.app_context():
    db.create_all()
#app.app_context().push()

#main page logo bar buttons
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login/")
def login():
    """username = request.form["username"]
    password = request.form["password"]
    user = Reg_Ind.query.filter_by(Username = username).first
    if user:
        Pass = Reg_Ind.query.filter(Reg_Ind.Password.has)
    sql = "SELECT password FROM users_table WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()
    
    if user:
        stored_password = user[0]  # Get the hashed password from the database

        # Verify the entered password with the stored hashed password
        if sha256_crypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session["username"] = username  # Store username in session
            return "Login successful! Welcome, " + username
        else:
            return "Invalid password. Try again."
    else:
        return "Username not found. Please register."""
    
    return render_template("login.html")

@app.route("/login/forgetpass")
def forget():
    return render_template("forget_password.html")

@app.route("/login/forgetpass/resetpass")
def resetpass():
    return render_template("reset_password.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/register/individual/", methods=['POST', 'GET'])
def Individual():
    if request.method == 'POST':
        Data = request.form['User']
        user = Reg_Ind.query.filter_by(Username = Data).first()
        if user:
            flash("Username already exists")
            return redirect('/register/individual/')
            
        
        Data2 = request.form['Email']
        email = Reg_Ind.query.filter_by(Email = Data2).first()
        if email:
            flash("Email already exists")
            return redirect('/register/individual/')
        
        Data3 = request.form['First']
        Data4 = request.form['Last']
        Data5 = request.form['Date']
        Data6 = sha256_crypt.encrypt(request.form['Pass'])
        Data7 = request.form['Code']

        #To verify
        #sha256_crypt.verify("Text Entered", where password stored in  database )
        #Will return True or False

        New_Data = Reg_Ind(Username = Data,Email = Data2, First_Name = Data3, Last_Name = Data4,DOB = Data5, Password = Data6, Code = Data7)
        try:
            db.session.add(New_Data)
            db.session.commit()
            return redirect('/login/')
        except:
            return ('Error')
    else:
        return render_template('RegInd.html')


@app.route('/register/organisation/', methods = ['POST', 'GET'])
def Organisation():
    if request.method == 'POST':
        Data = request.form['Org']
        Org_check = Reg_Org.query.filter_by(Org_Name = Data).first()
        if Org_check:
            flash("Organisation is already registered")
            return redirect('/register/organisation/')
        
        Data2 = request.form['Pro']
        Data3 = request.form['Cou']
        Data4 = request.form['Intro']

        Up_File = request.files['filename']
        filename = secure_filename(Up_File.filename)
        mimetype = Up_File.mimetype

        New_Data = Reg_Org(Org_Name = Data, Province = Data2, Country = Data3,Info = Data4, Logo_Img = Up_File.read() ,Logo_Name = filename,Logo_Mime = mimetype)

        try:
            db.session.add(New_Data)
            db.session.commit()
            return redirect("/register/individual/")
        except:
            return ('ERROR')
    else:
        return render_template('RegOrg.html')

#nav bar buttons
@app.route("/forums/")
def forums():
    return render_template("forums.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/volunteer/")
def volunteer():
    return render_template("volunteer.html")

@app.route("/discussion/")
def discussion():
    return render_template("discussion.html")

#testing privatemain template
@app.route("/privatemain/")
def privatemain():
    return render_template("PrivateMain.html")


if __name__ == "__main__":
    app.run(debug = True)
