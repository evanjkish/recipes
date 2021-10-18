from flask import Flask

app = Flask(__name__)
app.secret_key = "shhhhhh"

DATABASE = 'recipes_db'

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)