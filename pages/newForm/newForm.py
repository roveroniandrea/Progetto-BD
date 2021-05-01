from flask import Blueprint, render_template
from flask_login import login_required

newFormBlueprint = Blueprint('newForm', __name__)
"""Handles the routes to create a new form"""


@newFormBlueprint.route('/new', methods=['GET'])
@login_required
def newForm():
    return render_template('newForm/newForm.html')


@newFormBlueprint.route('/new', methods=['POST'])
@login_required
def submitNewForm():
    # TODO: submit form
    return render_template('newForm/formSubmitted.html')
