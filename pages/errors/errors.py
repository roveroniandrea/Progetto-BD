from flask import Blueprint, render_template, redirect

errorsBlueprint = Blueprint('errors', __name__)
"""Handles the various errors in routing"""


@errorsBlueprint.errorhandler(404)
def notFound(_):
    return render_template("404.html")


@errorsBlueprint.errorhandler(401)
def unhauthorized(_):
    return redirect('/login')
