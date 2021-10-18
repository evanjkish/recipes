from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import model_recipe
from flask_app.models import model_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login', methods = ['POST'])
def login():
    if not model_user.User.validate_login(request.form):
        redirect('/')
    user = model_user.User.get_one_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.hash_pw, request.form
    ['pw']):
        flash("Invalid password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/user/create', methods=['POST'])
def register():

    if not model_user.User.validate_registration(request.form):
        return redirect('/')

    if model_user.User.get_one_by_email(request.form):
        flash ("user already exists with email")
        return redirect('/')


    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "hash_pw" : bcrypt.generate_password_hash(request.form['pw'])
    }
    id = model_user.User.create(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['user_id']
    }
    return render_template("dashboard.html", user=model_user.User.get_one(data),
    recipes=model_recipe.Recipe.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')