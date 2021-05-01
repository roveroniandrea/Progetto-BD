from flask import Blueprint, render_template
from flask_login import login_required

newFormBlueprint = Blueprint('newForm', __name__)
"""Handles the routes to create a new form"""


@newFormBlueprint.route('/new', methods=['GET'])
@login_required
def newForm():
    return render_template('newForm.html')
