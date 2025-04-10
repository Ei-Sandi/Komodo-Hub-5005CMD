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
    
    @app.route("/mainpage/")
    def mainpage():
        return render_template("mainpage.html")

    @app.route("/volunteer/litter")
    def litter():
        return render_template("litter_picking.html")

    @app.route("/volunteer/feeding")
    def feeding():
        return render_template("animal_feeding.html")
    
    @app.route("/discussion/")
    def discussion():
        messages = Comments.query.order_by(Comments.timestamp.asc()).all()
        return render_template("discussion_pub.html", messages = messages)
    
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
    
    @app.route('/mammals')
    def mammals():
        return render_template('mammals.html')

    @app.route('/mammals/<species>')
    def mammals_species(species):
        species_data = {
            "sumatran_tiger": {
                "title": "Sumatran Tiger",
                "scientific_name": "Panthera Tigris Sumatrae",
                "status": "Critically Endangered",
                "description": ("Sumatran tigers, native to Indonesia's Sumatra Island, are critically endangered "
                                "due to habitat loss, poaching, and human-wildlife conflict. "
                                "Deforestation for palm oil plantations and illegal logging has fragmented their habitat, "
                                "while poaching for body parts and prey depletion further threaten their survival. "
                                "Conservation efforts include anti-poaching initiatives, habitat restoration, and community engagement."),
                "images": ["images/sumatran_tiger1.jpeg",
                    "images/sumatran_tiger2.jpeg",
                    "images/sumatran_tiger3.jpeg",
                    "images/sumatran_tiger4.jpeg",
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

    @app.route('/birds')
    def birds():
        return render_template('birds.html')
    
    @app.route('/birds/<species>')
    def birds_species(species):
        species_data = {
            "blue_fronted_lorikeet" : {
            "title": "Blue-Fronted Lorikeet",
            "scientific_name": "Charmosyna Toxopei",
            "status": "Vulnerable",
            "description": ("The Blue-Fronted Lorikeet, endemic to Indonesia, is classified as Vulnerable due to habitat loss "
                                "from deforestation and illegal trapping for the pet trade. "
                                "Conservation efforts include habitat protection and community awareness programs."),
            "images": ["images/blue_fronted_lorikeet1.jpg",
                    "images/blue_fronted_lorikeet2.jpg",
                    "images/blue_fronted_lorikeet3.jpg",
                    "images/blue_fronted_lorikeet4.jpg",
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

    @app.route('/amphibians')
    def amphibians():
        return render_template('amphibians.html')
    
    @app.route('/amphibians/<species>')
    def amphibians_species(species):
        species_data = {
            "bornean_flat_headed_frog": {
                "title": "Bornean Flat-Headed Frog",
                "scientific_name": "Barbourula Kalimantanensis",
                "status": "Critically Endangered",
                "description": ("The Bornean Flat-Headed Frog, native to Borneo, is critically endangered due to habitat loss "
                                "from deforestation and pollution. "
                                "Conservation efforts focus on habitat protection and raising awareness about its plight."),
                "images": ["images/bornean_flat_headed_frog1.jpg",
                    "images/bornean_flat_headed_frog2.jpg",
                    "images/bornean_flat_headed_frog3.jpg",
                    "images/bornean_flat_headed_frog4.jpg",
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
    
    @app.route('/fish')
    def fish():
        return render_template('fish.html')
    
    @app.route('/fish/<species>')
    def fish_species(species):
        species_data = {
            "featherback_knifefish": {
                "title": "Featherback/Knifefish",
                "scientific_name": "Chitala Chitala",
                "status": "Vulnerable",
                "description": ("The Featherback/Knifefish, native to Southeast Asia, is vulnerable due to habitat loss "
                                "from deforestation and pollution. "
                                "Conservation efforts focus on habitat protection and sustainable fishing practices."),
                "images": ["images/featherback_knifefish1.jpg",
                    "images/featherback_knifefish2.jpg",
                    "images/featherback_knifefish3.jpg",
                    "images/featherback_knifefish4.jpg",
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
    
    @app.route('/invertebrates')
    def invertebrates():
        return render_template('invertebrates.html')
    
    @app.route('/invertebrates/<species>')
    def invertebrates_species(species):
        species_data = {
            "coconut_crabs": {
                "title": "Coconut Crabs",
                "scientific_name": "Birgus Latro",
                "status": "Vulnerable",
                "description": ("Coconut crabs, native to tropical islands, are vulnerable due to habitat loss "
                                "from deforestation and overharvesting. "
                                "Conservation efforts focus on habitat protection and sustainable harvesting practices."),
                "images": ["images/coconut_crabs1.jpg",
                    "images/coconut_crabs2.jpg",
                    "images/coconut_crabs3.jpg",
                    "images/coconut_crabs4.jpg",
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
    
    @app.route("/sighting/")
    def sighting():
        return render_template("sighting.html")
    
    @app.route("/donation/")
    def donation():
        return render_template("donation.html")
    
    @app.route("/Animal/")
    def Animal():
        return render_template("Animal.html")
    
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
        if current_user.role == 'principal':
            return redirect(url_for("principal_dashboard"))
        elif current_user.role == 'student':
            return render_template("student_dashboard.html", username = session['username'])
        # elif current_user.role == 'teacher':
        #     return render_template("teacher_dashboard.html", username = session['username'])
        else:
            return render_template("dashboard.html", username = session['username'])
        
    @app.route("/dashboard/discussion_priv/", methods=['GET', 'POST'])
    @login_required
    def discussion_priv():
        socketio = SocketIO(app, cors_allowed_origins="*")
        history = Comments.query.order_by(Comments.timestamp.asc()).all()

        @socketio.on('message')
        def get_comment(data):
            username = current_user.username
            message = data.get("message")

            if not message.strip():
                return

            new_comment = Comments(username=username, comment=message, timestamp=datetime.now())
            db.session.add(new_comment)
            db.session.commit()

            socketio.emit('new_message', {
                "username": username,
                "message": message,
                "timestamp": new_comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "cmt_id": new_comment.cmt_id
            })

        @socketio.on('delete_message')
        def delete_message(data):
            socketio = SocketIO(app, cors_allowed_origins="*")
            comment_id = data.get("cmt_id")
            username = current_user.username

            if not comment_id:
                return

            comment = Comments.query.get(comment_id)

            if comment and comment.username == username:
                db.session.delete(comment)
                db.session.commit()

                socketio.emit('message_deleted', {"cmt_id": comment_id})

        @socketio.on('message')
        def get_comment(data):
            username = current_user.username
            message = data.get("message")
            reply_id = data.get("reply_id")

            if not message.strip():
                return

            new_comment = Comments(username=username, comment=message, timestamp=datetime.now(), reply_id=reply_id)
            db.session.add(new_comment)
            db.session.commit()

            socketio.emit('new_message', {
                "username": username,
                "message": message,
                "timestamp": new_comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "cmt_id": new_comment.cmt_id,
                "reply_id": reply_id
            })

        return render_template("discussion_priv.html", messages=history)
        
    @app.route("/classroom/")
    @login_required
    def classroom():
        if current_user.role == 'student':
            return render_template ("student_classroom.html")
        else:
            return render_template ("teacher_classroom.html")
    

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
    

def principal_routes(app):
    @app.route("/principal/", methods = ['GET','POST'])
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
            elif user.role not in ['student', 'teacher']:
                #need to fix error message here
                return jsonify({"message": "You don't have access to this user.", "redirect": url_for("principal_dashboard")})
            else:
                role = request.form.get("role")
                user.role = role
                user.org_id = current_user.org_id
                db.session.commit()
                return redirect(url_for("principal_dashboard"))
            
    @app.route('/get_graph/<string:graph_type>', methods=['GET'])
    def get_graph(graph_type):
        graphs = {
            "user_behaviour": {"title": "User Behaviour Graph", "data": [10, 20, 30, 40]},
            "user_demography": {"title": "User Demography Graph", "data": [15, 25, 35, 45]},
            "subscriptions": {"title": "Subscriptions Graph", "data": [50, 60, 70, 80]},
            "service_availability": {"title": "Service Availability Graph", "data": [40, 50, 30, 20]},
            "service_popularity": {"title": "Service Popularity Graph", "data": [5, 15, 25, 35]},
            "maintenance_reports": {"title": "Maintenance/Reports Graph", "data": [8, 18, 28, 38]}
        }
        return jsonify(graphs.get(graph_type, {"error": "Graph not found"}))


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
    
    @app.route("/dashboard/volunteer_priv/")
    def volunteer_priv():
        return render_template("volunteer_priv.html")
    
    @app.route("/dashboard/volunteer_priv/feeding_priv")
    def feeding_priv():
        return render_template("animal_feeding_priv.html")
    
    @app.route("/dashboard/volunteer/litter_priv")
    def litter_priv():
        return render_template("litter_picking_priv.html")
    
    @app.route("/donation_priv/")
    def donation_priv():
        return render_template("donation_priv.html")
    
    @app.route("/sighting_priv/")
    def sighting_priv():
        return render_template("sighting_priv.html")
    
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


    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        user = User.query.get(current_user.uid)
        org = None

        if user.org_id:
            org = Organisation.query.get(user.org_id)

        if request.method == 'POST':
            new_username = request.form.get('username')
            if new_username != user.username:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user:
                    flash('Username already taken please choose another', 'error')
                    return redirect(url_for('edit_profile'))
                user.username = new_username
            user.email = request.form.get('email')
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')

            if org:
                org.org_name = request.form.get('org_name')
                org.province = request.form.get('province')
                org.country = request.form.get('country')

            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('edit_profile'))

        return render_template('edit_profile.html', user=user, org=org)



