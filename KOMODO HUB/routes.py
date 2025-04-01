from flask import render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, join_room, leave_room, send
import random, string

def all_routes(app):
    @app.route("/")
    @app.route("/home/")
    def home():
        if current_user.is_authenticated:
            username = current_user.username
            return redirect(url_for("dashboard", username=username))
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
    
    @app.route("/student_classroom/")
    def student_classroom():
        return render_template("student_classroom.html")
    
    @app.route("/teacher_classroom/")
    def teacher_classroom():
        return render_template("teacher_classroom.html")
    
    @app.route('/week_s/')
    def week_s():
        course = request.args.get('course')
        # Fetch course data from database
        return render_template('week_s.html', course_name=course)
    
    @app.route('/admin/')
    def admin():
        return render_template("admin.html")

    @app.route('/upload', methods=['POST'])
    def upload():
        # Handle file upload logic
        return redirect(url_for('submission_success'))

    @app.route('/api/upload', methods=['POST'])
    def api_upload():
        # Handle API upload logic
        return jsonify(success=True)
    
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
            org = None
            if 'orgName' in session:
                newOrg = Organisation(org_name = session['orgName'],province = session['province'], country = session['country'], intro = session['intro'], access_code = session['access'])
                db.session.add(newOrg)
                db.session.commit()
                role = 'principal'
                org = Organisation.query.filter(Organisation.org_name == session['orgName']).first()

            username = request.form['username']
            email = request.form['email']
            firstName = request.form['first']
            lastName = request.form['last']
            dob = request.form['dob']
            password = request.form['Pass']
            hashed_password = bcrypt.generate_password_hash(password)
            org_id = org.org_id if org else None
            if org:
                pass
            else:
                code = request.form['code']
                org = Organisation.query.filter(Organisation.access_code == code).first()
                org_id = org.org_id if org else None

            #add new user into database
            new_user = User(username = username,email = email, first_name = firstName, last_name = lastName, dob = dob, password = hashed_password, role = role, org_id = org_id)
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
    
    @app.route('/validate-accesscode/', methods = ['POST'])
    def validate_accesscode():
        if request.method == 'POST':
            access = request.get_json()['code']
            access_code = Organisation.query.filter(Organisation.access_code == access).first()
            if access_code:
                return jsonify({'code_exists' : 'true'})
            else:
                return jsonify({'code_exists' : 'false'})  
            
    @app.route('/register/organisation/', methods = ['POST', 'GET'])
    def organisation():
        if request.method == 'GET':
            return render_template('RegOrg.html')
        if request.method == 'POST':
            session['orgName'] = request.form['orgName']
            session['province'] = request.form['province']
            session['country'] = request.form['country']
            session['intro'] = request.form['intro']
            session['access'] = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
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
    @app.route("/dashboard/")
    @login_required
    def dashboard():
        if "username" in session:
            return render_template("dashboard.html", username = session['username'])
        if current_user.role == 'principal':
                return redirect(url_for("principal_dashboard"))
        else:
            return render_template("dashboard.html", username = session['username'])

    @app.route('/Room1/')
    @login_required
    def chat_room1():
        socketio = SocketIO(app, cors_allowed_origins="*")
        username = current_user.username
        @socketio.on('message')
        def handle_message(message):
            print("Message Recieved " + message)
            msg = Room1(Message= username +  message)
            db.session.add(msg)
            db.session.commit()

            if message != "Connected":
                send(message, broadcast=True)

        message_history = Room1.query.all() 
        return render_template("Room1.html", message=message_history)

    @app.route('/Room2/')
    @login_required
    def chat_room2():
        socketio = SocketIO(app, cors_allowed_origins="*")
        username = current_user.username
        @socketio.on('message')
        def handle_message(message):
            print("Message Recieved " + message)
            msg = Room2(Message= username +  message)
            db.session.add(msg)
            db.session.commit()

            if message != "Connected":
                send(message, broadcast=True)

        message_history = Room2.query.all() 
        return render_template("Room1.html", message=message_history)
    
    @app.route('/Room3/')
    @login_required
    def chat_room3():
        socketio = SocketIO(app, cors_allowed_origins="*")
        username = current_user.username
        @socketio.on('message')
        def handle_message(message):
            print("Message Recieved " + message)
            msg = Room3(Message= username +  message)
            db.session.add(msg)
            db.session.commit()

            if message != "Connected":
                send(message, broadcast=True)

        message_history = Room3.query.all() 
        return render_template("Room1.html", message=message_history)
            
    @app.route("/pm_mess/", methods=['POST', 'GET'])
    @login_required
    def pm_mess():
        username = current_user.username
        roles = User.query.filter(User.username == username).first()
        socketio = SocketIO(app, cors_allowed_origins="*")

        @socketio.on('message')
        def handle_message(message):
            print("Message Received " + message)
            msg = Messages(Message= username +  message)
            db.session.add(msg)
            db.session.commit()

            if message != "Connected":
                send(message, broadcast=True)

        if request.method == "POST":
            room=request.form["room"]

            if room=="Room1":
                if "student" == roles.role:
                    return redirect("/Room1/")
                else:
                    flash("You can't join this room")
                    return redirect("/pm_mess/")
            if room=="Room2":
                if "teacher" in roles.role:
                    return redirect("/Room2/")
                else:
                    flash("You can't join this room")
                    return redirect("/pm_mess/")
            if room=="Room3":
                if "principal" == roles.role:
                    return redirect("/Room3/")
                else:
                    flash("You can't join this room")
                    return redirect("/pm_mess/")
            
        message_history = Messages.query.all() 
        return render_template("pm_mess.html", message = message_history)
    
    @app.route('/chat_room/', methods=['POST', 'GET'])
    @login_required
    def chat_room():
        socketio = SocketIO(app, cors_allowed_origins="*")

        @socketio.on('message')
        def handle_message(message):
            print("Message Recieved " + message)
            if message != "Connected":
                send(message, broadcast=True)

        return render_template("chat_room.html")

def principal_routes(app):
    @app.route("/principal/user/", methods = ['GET','POST'])
    @login_required
    def principal_dashboard():
        if request.method == 'GET':
            org = Organisation.query.filter(Organisation.org_id == current_user.org_id).first()
            org_name = org.org_name
            access_code = org.access_code
            return render_template("principal_user.html", username = current_user.username, org_name = org_name, access = access_code)
        elif request.method == 'POST':
            username = request.form.get("username")
            user = User.query.filter(User.username == username).first()
            if not user:
                return redirect(url_for("principal_dashboard"))            
            elif user.org_id != current_user.org_id:
                #need to fix error message here
                return jsonify({"message": "You don't have access to this user.", "redirect": url_for("principal_dashboard")})
            elif user.role not in ['student', 'teacher']:
                #need to fix error message here
                return jsonify({"message": "You don't have access to this user.", "redirect": url_for("principal_dashboard")})
            else:
                role = request.form.get("role")
                user.role = role
                user.org_id = current_user.org_id
                db.session.commit()
                return redirect(url_for("principal_dashboard"))

    @app.route("/principal/org/", methods = ['GET','POST'])
    @login_required        
    def principal_org():
        if request.method == 'GET':
            org = Organisation.query.filter(Organisation.org_id == current_user.org_id).first()
            org_name = org.org_name
            province = org.province
            country = org.country
            access_code = org.access_code
            description = org.intro
            return render_template("principal_org.html", username = current_user.username, org_name = org_name, access = access_code, province = province, country = country, description = description)
        elif request.method == 'POST':
            org_name = request.form.get("org_name")
            province = request.form.get("province")
            country = request.form.get("country")
            description = request.form.get("description")

            org = Organisation.query.filter(Organisation.org_id == current_user.org_id).first()
            org.org_name = org_name
            org.province = province
            org.country = country
            org.into = description
            db.session.commit()
            return redirect(url_for("principal_org"))

    @app.route('/save_access_code', methods=['POST'])
    def save_access_code():
        data = request.json
        access_code = data.get('access_code')

        if not access_code:
            return jsonify({"message": "No access code received"}), 400
        
        org = Organisation.query.filter(Organisation.org_id == current_user.org_id).first()
        org.access_code = access_code
        db.session.commit()

        return jsonify({"message": f"Access Code '{access_code}' saved successfully!", "redirect": url_for("principal_org")})

    
    @app.route('/activity/')
    @login_required
    def activity():
        return render_template("Activities.html")
    
    @app.route('/games/')
    @login_required
    def games():
        return render_template("Games.html")
    
    @app.route('/quizzes/')
    @login_required
    def quizzes():
        return render_template("Quizzes.html")
    
    @app.route('/design/')
    @login_required
    def design():
        return render_template("Design.html")
    
    @app.route('/quiz1/', methods=["POST", "GET"])
    @login_required
    def quiz1():
        if request.method == "POST":
            username = current_user.username
            Score = 0
            Answer1 = request.form['Q1']
            Answer2 = request.form['Q2']
            Answer3 = request.form['Q3']
            Answer4 = request.form['Q4']
            Answer5 = request.form['Q5']

            if Answer1 == "ans2":
                Score += 1
            if Answer2 == "ans1":
                Score += 1
            if Answer3 == "ans3":
                Score += 1
            if Answer4 == "ans2":
                Score += 1
            if Answer5 == "ans4":
                Score += 1

            score = Quiz1(username = username, score = Score)
            db.session.add(score)
            db.session.commit()
            
            flash("Your score is " + str(Score) + " out of 5")
            return redirect("/quiz1/")
        return render_template("Quiz1.html")



