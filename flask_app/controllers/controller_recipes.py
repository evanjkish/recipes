from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models import model_recipe
from flask_app.models import model_user




@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }

    return render_template('add_recipe.html', user=model_user.User.get_one(data))

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('logout')
    if not model_recipe.Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name":request.form["name"],
        "description":request.form["description"],
        "instruction":request.form["instruction"],
        "under_thirty":int(request.form["under_thirty"]),
        "date_made":request.form["date_made"],
        "user_id":session["user_id"]
    }
    model_recipe.Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    edit=model_recipe.Recipe.get_one(data)
    if edit.user_id != user_data['id']:
        return redirect('/dashboard')
    return render_template("edit_recipe.html", edit=edit,
    user=model_user.User.get_one(user_data))

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not model_recipe.Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name":request.form["name"],
        "description":request.form["description"],
        "instruction":request.form["instruction"],
        "under_thirty":int(request.form["under_thirty"]),
        "date_made":request.form["date_made"],
        "id":request.form["id"]
    }
    model_recipe.Recipe.update_one(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_recipe.html", recipe=model_recipe.Recipe.get_one(data),
    user=model_user.User.get_one(user_data))



@app.route('/destroy/recipe/<int:id>/')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    model_recipe.Recipe.destroy(data)
    return redirect('/dashboard')
    