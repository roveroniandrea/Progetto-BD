from flask import Blueprint, render_template
from flask_login import login_required, current_user

from lib.initDB import Session

homeBlueprint = Blueprint('home', __name__)
"""Handles the home route"""


@homeBlueprint.route('/', methods=['GET'])
@login_required
def home():
    session = Session()
    user = session.merge(current_user)
    my_forms = []
    answered_forms = []
    unanswered_forms = []
    for access in user.accessesRel:
        form = access.formRel
        if form.owner == user.email:
            my_forms.append(form)
        elif access.access_id is None:
            unanswered_forms.append(form)
        else:
            answered_forms.append(form)
    session.close()
    return render_template('home.html', my_forms=my_forms, answered_forms=answered_forms,
                           unanswered_forms=unanswered_forms)
