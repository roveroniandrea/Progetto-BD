from flask import Flask, render_template, redirect
from flask_login import LoginManager

from lib.DB_API import loadUser
from pages.home.home import homeBlueprint
from pages.login.login import loginBlueprint

app = Flask(__name__)
"""The running app"""

app.secret_key = 'super_secret_key'

loginManager = LoginManager()
"""The login manager sets the routes of the application"""

loginManager.init_app(app)


@loginManager.user_loader
def load_user(user_id):
    return loadUser(user_id)


# TODO: don't know if this line is required
loginManager.user_loader(load_user)

app.register_blueprint(loginBlueprint)
app.register_blueprint(homeBlueprint)


@app.errorhandler(404)
def notFound(_):
    return render_template("404.html")


@app.errorhandler(401)
def unhauthorized(_):
    print("Hola")
    return redirect('/login')
