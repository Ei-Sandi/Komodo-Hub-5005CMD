from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

#main page logo bar buttons
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route('/Organisation/')
def Organisation():
    return render_template('RegOrg.html')

@app.route('/Individual/')
def Individual():
    return render_template('RegInd.html')

#nav bar buttons
@app.route("/news/")
def news():
    return render_template("news.html")

@app.route("/forums/")
def forums():
    return render_template("forums.html")

@app.route("/about-us/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug = True)
