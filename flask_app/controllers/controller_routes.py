from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_recipe
from flask_app.models import model_user

# from flask_app.models import

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')


@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'