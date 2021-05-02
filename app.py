from flask import Flask, render_template, redirect
from flask_login import LoginManager

from lib.UserAPI import loadUser
from pages.formPage.formPage import formPageBlueprint
from pages.home.home import homeBlueprint
from pages.auth.auth import authBlueprint
from pages.newForm.newForm import newFormBlueprint

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

app.register_blueprint(authBlueprint)
app.register_blueprint(homeBlueprint)
app.register_blueprint(newFormBlueprint)
app.register_blueprint(formPageBlueprint)


@app.errorhandler(404)
def notFound(_):
    return render_template("404.html")


@app.errorhandler(401)
def unhauthorized(_):
    return redirect('/login')
