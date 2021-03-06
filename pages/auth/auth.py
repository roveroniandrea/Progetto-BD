from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from lib.UserAPI import validateUser, registerUser


def redirectToHomeIfAuth(cb):
    """Redirects to home if the user is logged in, otherwise executes the callback"""
    if current_user.is_authenticated:
        return redirect('/')
    else:
        return cb()


authBlueprint = Blueprint('auth', __name__)
"""Handles the auth and logout routes"""


@authBlueprint.route('/login', methods=['GET'])
def login():
    return redirectToHomeIfAuth(lambda: render_template('auth/login.html'))


@authBlueprint.route('/login', methods=['POST'])
def handleLogin():
    user = validateUser(request.form['email'], request.form['password'])
    if user:
        login_user(user)
        return redirect('/')
    return render_template('auth/login.html', error="Nessun utente trovato!")


@authBlueprint.route('/logout', methods=['POST'])
@login_required
def handleLogout():
    logout_user()
    return redirect('/')


@authBlueprint.route('/register', methods=['GET'])
def register():
    return redirectToHomeIfAuth(lambda: render_template('auth/register.html'))


@authBlueprint.route('/register', methods=['POST'])
def handleRegister():
    if registerUser(request.form['email'], request.form['password']):
        user = validateUser(request.form['email'], request.form['password'])
        login_user(user)
        return redirect('/')
    return render_template('auth/register.html', error="L'utente esiste già")
