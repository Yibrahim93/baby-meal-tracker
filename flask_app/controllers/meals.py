from flask_app import app
from flask import render_template, redirect,session, request
from flask_app.models import meal

@app.route('/meal/new')
def new_meal():
    # if "user_id" not in session:
    #     return redirect("/")
    # data = {
    #     "id": id
    # }
    return render_template('newmeal.html')

@app.route('/meal/create', methods=['POST'])
def create_meal():
    if not meal.Meal.validate_newmeal(request.form):
        return redirect('/meal/new')
    if "user_id" not in session:
        return redirect("/")
    # show.Show.save(request.form)
    # return redirect('/dashboard')
    else:
        data = {
            "meal": request.form["meal"],
            "date": request.form["date"],
            "time": request.form["time"],
            "liked": request.form["liked"],
            "description": request.form["description"],
            "user_id": session["user_id"],
        }
        meal.Meal.save(data)
        return redirect('/dashboard')

@app.route("/meal/<int:id>")
def view_meal(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }    
    return render_template("showmeal.html", meal = meal.Meal.get_onemeal(data))


@app.route('/delete/<int:id>')
def delete_meal(id):
    meal.Meal.delete_meal(id)
    return redirect ('/dashboard')


@app.route("/meal/<int:id>/update", methods=["POST"]) 
def update(id):
    if "user_id" not in session:
        return redirect("/")
    if not meal.Meal.validate_newmeal(request.form):
        return redirect(f"/meal/{id}/edit")
    else:
        data = {
            "meal": request.form["meal"],
            "date": request.form["date"],
            "time": request.form["time"],
            "liked": request.form["liked"],
            "description": request.form["description"],
            "id":id
        }
        meal.Meal.edit_meal(data)
        return redirect('/dashboard')

@app.route('/meal/<int:id>/edit')
def edit_meal(id):
    if "user_id" not in session:
        return redirect("/")
    data = {

            "id":id
        }
    return render_template('editmeal.html', meal = meal.Meal.get_onemeal(data))
