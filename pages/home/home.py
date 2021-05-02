from flask import Blueprint, render_template
from flask_login import login_required

homeBlueprint = Blueprint('home', __name__)
"""Handles the home route"""


@homeBlueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')
