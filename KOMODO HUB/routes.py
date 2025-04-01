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
    
    @app.route('/animals')
    def animals():
        return render_template('animals.html')

    @app.route('/species/<name>')
    def species(name):
        return render_template('species.html', species_name=name)
    
    @app.route('/reptiles')
    def reptiles():
        return render_template('reptiles.html')

    @app.route('/reptiles/<species>')
    def reptile_species(species):
        species_data = {
            "komodo_dragon": {
                "title": "Komodo Dragon",
                "scientific_name": "Varanus Komodoensis",
                "status": "Endangered",
                "description": ("Komodo dragons, found only on a few Indonesian islands, are classified "
                                "as Endangered due to habitat loss, climate change, and human activities. "
                                "Rising sea levels and land development threaten their habitat, "
                                "while declining prey populations and poaching further impact their survival. "
                                "Human-dragon conflicts also pose risks as encounters increase. Conservation efforts, "
                                "including Komodo National Park, anti-poaching laws, and ecotourism, aim to protect them, "
                                "but climate change remains a major long-term threat."),
                "images": [
                    "images/komodo_dragon1.jpeg",
                    "images/komodo_dragon2.jpeg",
                    "images/komodo_dragon3.jpeg",
                    "images/komodo_dragon4.jpeg",
                ]
            }
        }
        data = species_data.get(species)
        if data:
            return render_template(
                'species.html', 
                species_name=data["title"], 
                scientific_name=data["scientific_name"], 
                status=data["status"], 
                description=data["description"],
                images=data["images"]
            )  
        return render_template('404.html')

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
            username = request.form['username']
            email = request.form['email']
            firstName = request.form['first']
            lastName = request.form['last']
            dob = request.form['dob']
            password = request.form['Pass']
            hashed_password = bcrypt.generate_password_hash(password)
            code = request.form['code']

            #check if username already exists
            userCheck = User.query.filter(User.username == username).first()
            if userCheck:
                return redirect(url_for("individual"))
            
            #check if email already exists
            emailCheck = User.query.filter(User.email == email).first()
            if emailCheck:
                return redirect(url_for("individual"))

            #add new user into database
            new_user = User(username = username,email = email, first_name = firstName, last_name = lastName, dob = dob, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
    @app.route('/register/organisation/', methods = ['POST', 'GET'])
    def organisation():
        if request.method == 'GET':
            return render_template('RegOrg.html')
        if request.method == 'POST':
            orgName = request.form['orgName']
            province = request.form['province']
            country = request.form['country']
            intro = request.form['intro']
            logo = request.files['filename']
            filename = secure_filename(logo.filename)
            mimetype = logo.mimetype

            newOrg = Organisation(org_name = orgName, province = province, country = country, intro = intro, logo_img = logo.read() , logo_name = filename, logo_type = mimetype)

            db.session.add(newOrg)
            db.session.commit()
            return redirect("/register/individual/")
        
def login_routes(app, bcrypt):        
    @app.route("/login/", methods=["GET", "POST"])
    def login():  
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password,password):
                login_user(user)
                session["username"] = username
                return redirect(url_for("home"))
            else:
                return redirect(url_for("login"))

    @app.route("/login/forgetpass")
    def forget():
        return render_template("forget_password.html")

    @app.route("/login/forgetpass/resetpass")
    def resetpass():
        return render_template("reset_password.html")
    
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("home"))
    
def restricted_routes(app):
    @app.route("/dashboard")
    @login_required
    def dashboard():
        if "username" in session:
            return render_template("dashboard.html", username = session['username'])
        
    @login_required    
    @app.route("/PM_Mess/")
    def PM_Mess():
        message_history = Messages.query.all() 
        return render_template("PM_Mess.html", message = message_history)



