from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, meal
# visible routes

@app.route("/")
def index_route():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        data = {
            "id": session["user_id"]
        }
        return render_template ("dashboard.html", user = user.User.grab_userid(data), meals = meal.Meal.get_meals())
    else:
        return redirect("/")


@app.route("/new")
def new_route():
    return render_template("newmeal.html")

# invisible routes
@app.route("/register", methods=["POST"]) #button to register a new route
def register_user():
    if not user.User.validate_newuser(request.form):
        return redirect("/")
    else:
        data = {
            "first_name": request.form ['first_name'],
            "last_name": request.form['last_name'],
            "relation": request.form['relation'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password']),
            }
        session["user_id"]= user.User.register(data)
        return redirect ("/dashboard")

@app.route("/login", methods=["POST"]) #button
def login_user():
    if not user.User.validate_login(request.form):
        return redirect("/")
    else:
        email_data = {
            "email": request.form["email"]
        }
    found_user = user.User.grab_useremail(email_data)
    session["user_id"] = found_user.id
    session["relation"] = found_user.relation
    return redirect("/dashboard")

@app.route("/logout") #clear session then send to the reg/login page via root route
def logout():
    session.clear()
    return redirect("/")