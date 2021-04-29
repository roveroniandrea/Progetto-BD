from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from lib.DB_API import validateUser

loginBlueprint = Blueprint('auth', __name__)
"""Handles the login and logout routes"""


@loginBlueprint.route('/login', methods=['GET'])
def login():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        return redirect('/')


@loginBlueprint.route('/login', methods=['POST'])
def handleLogin():
    user = validateUser(request.form['email'], request.form['password'])
    if user:
        login_user(user)
        return redirect('/')
    return render_template('login.html', error="Nessun utente trovato!")


@loginBlueprint.route('/logout', methods=['POST'])
@login_required
def handleLogout():
    logout_user()
    return redirect('/login')
