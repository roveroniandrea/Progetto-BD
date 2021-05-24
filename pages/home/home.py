from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from pages.home.addFormAccess import getFormAccesses, addFormAccess
from lib.initDB import Session

homeBlueprint = Blueprint('home', __name__)
"""Handles the home route"""


@homeBlueprint.route('/', methods=['GET'])
def home():
    """The home page"""
    if current_user.is_authenticated:
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

        my_forms.sort(key=lambda f: f.creation_date, reverse=True)
        answered_forms.sort(key=lambda f: f.creation_date, reverse=True)
        unanswered_forms.sort(key=lambda f: f.creation_date, reverse=True)

        template = render_template('home.html', my_forms=my_forms, answered_forms=answered_forms,
                                   unanswered_forms=unanswered_forms, user=current_user)
        session.close()
        return template
    else:
        return redirect('/login')


@homeBlueprint.route('/q/<int:form_id>/accesses', methods=['GET'])
@login_required
def defGetFormAccesses(form_id):
    return getFormAccesses(form_id)


@homeBlueprint.route('/q/<int:form_id>/accesses/<string:email>', methods=['POST'])
@login_required
def defAddFormAccess(form_id, email):
    return addFormAccess(form_id, email)
