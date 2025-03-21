from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from werkzeug.utils import secure_filename

def all_routes(app):
    @app.route("/")
    @app.route("/home/")
    def home():
        if current_user.is_authenticated:
            username = current_user.username
            role = current_user.role
            return redirect(url_for("dashboard", username=username, role=role))
        else:
            return render_template("home.html")
    
    @app.route("/forums/")
    def forums():
        return render_template("forums.html")

    @app.route("/contact/")
    def contact():
        return render_template("contact.html")

    @app.route("/volunteer/")
    def volunteer():
        return render_template("volunteer.html")

    @app.route("/volunteer/litter")
    def litter():
        return render_template("litter_picking.html")

    @app.route("/volunteer/feeding")
    def feeding():
        return render_template("animal_feeding.html")
    
    @app.route("/discussion/")
    def discussion():
        return render_template("discussion.html")
    
    #testing privatemain template
    @app.route("/privatemain/")
    def privatemain():
        return render_template("PrivateMain.html")
    
def register_routes(app, db, bcrypt):
    @app.route("/register/")
    def register():
        return render_template("register.html")
    
    @app.route("/register/individual/", methods=['POST', 'GET'])
    def individual():    
        if request.method == 'GET':
            return render_template('RegInd.html')
        elif request.method == 'POST':
            role = 'student'

            if 'orgName' in session:
                newOrg = Organisation(org_name = session['orgName'],province = session['province'], country = session['country'], intro = session['intro'])
                role = 'principal'
                db.session.add(newOrg)
                db.session.commit()

            username = request.form['username']
            email = request.form['email']
            firstName = request.form['first']
            lastName = request.form['last']
            dob = request.form['dob']
            password = request.form['Pass']
            hashed_password = bcrypt.generate_password_hash(password)
            code = request.form['code']

            #add new user into database
            new_user = User(username = username,email = email, first_name = firstName, last_name = lastName, dob = dob, password = hashed_password, role = role)
            db.session.add(new_user)
            db.session.commit()
            session.clear()
            return redirect(url_for('login'))
    
    @app.route('/validate-email-registration/', methods = ['POST'])
    def validate_email_registration():
        if request.method == 'POST':
            email = request.get_json()['email']
            email = User.query.filter(User.email == email).first()
            if email:
                return jsonify({'email_exists' : 'true'})
            else:
                return jsonify({'email_exists' : 'false'})
    
    @app.route('/validate-username-registration/', methods = ['POST'])
    def validate_username_registration():
        if request.method == 'POST':
            username = request.get_json()['username']
            username = User.query.filter(User.username == username).first()
            if username:
                return jsonify({'username_exists' : 'true'})
            else:
                return jsonify({'username_exists' : 'false'})

    @app.route('/register/organisation/', methods = ['POST', 'GET'])
    def organisation():
        if request.method == 'GET':
            return render_template('RegOrg.html')
        if request.method == 'POST':
            session['orgName'] = request.form['orgName']
            session['province'] = request.form['province']
            session['country'] = request.form['country']
            session['intro'] = request.form['intro']
            #logo = request.files['filename']
            #if logo:
                #session['logo'] = logo.read() #read the image as binary
                #session['mimetype'] = logo.content_type #get MIME type of logo

            return redirect("/register/individual/")
        
    @app.route('/validate-orgname-registration/', methods = ['POST'])
    def validate_orgname_registration():
        if request.method == 'POST':
            orgname = request.get_json()['orgname']
            orgname = Organisation.query.filter(Organisation.org_name == orgname).first()
            if orgname:
                return jsonify({'orgname_exists' : 'true'})
            else:
                return jsonify({'orgname_exists' : 'false'})
        
def login_routes(app, bcrypt):        
    @app.route("/login/", methods=["GET", "POST"])
    def login():  
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(User.username == username).first()
            if not user:
                return redirect(url_for("register"))
            elif bcrypt.check_password_hash(user.password,password):
                login_user(user)
                session["username"] = username
                return redirect(url_for("home"))
            else:
                return redirect(url_for("login"))

    @app.route('/check-password/', methods = ['POST'])
    def checkPassword():
        if request.method == 'POST':
            username = request.get_json()['username']
            password = request.get_json()['password']
            user = User.query.filter(User.username == username).first()
            
            if user and bcrypt.check_password_hash(user.password,password):
                return jsonify({'password_match' : 'true'})
            else:
                return jsonify({'password_match' : 'false'})

    @app.route("/login/forgetpass")
    def forget():
        return render_template("forget_password.html")

    @app.route("/login/forgetpass/resetpass")
    def resetpass():
        return render_template("reset_password.html")
    
    @app.route("/logout")
    def logout():
        logout_user()
        session.clear()
        return redirect(url_for("home"))
    
def restricted_routes(app):
    @app.route("/dashboard")
    @login_required
    def dashboard():
        if "username" in session:
            return render_template("dashboard.html", username = session['username'])
        
    @app.route("/PM_Mess/")
    @login_required
    def PM_Mess():
        message_history = Messages.query.all() 
        return render_template("PM_Mess.html", message = message_history)
    



