import json

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from lib.initDB import Session
from lib.types.Access import Access
from lib.types.Form import Form
from lib.types.Question import Question

newFormBlueprint = Blueprint('newForm', __name__)
"""Handles the routes to create a new form"""


@newFormBlueprint.route('/new', methods=['GET'])
@login_required
def newForm():
    return render_template('newForm/newForm.html')


@newFormBlueprint.route('/new', methods=['POST'])
@login_required
def submitNewForm():
    session = Session()
    form_data = json.loads(request.form['data'])

    try:
        user = session.merge(current_user)
        form = Form()
        form.ownerUserRel = user
        form.owner = user.email
        form.title = form_data['title']
        form.color = form_data['color']
        session.add(form)
        for submitted_question in form_data['questions']:
            question = Question()
            question.formRel = form
            question.question = submitted_question['question']
            question.type = submitted_question['type']
            question.options = submitted_question['options']
            question.required = submitted_question['required']

        access = Access()
        access.userRel = user
        access.formRel = form

        for submitted_access in form_data['accesses']:
            access = Access()
            access.user = submitted_access
            access.formRel = form

        session.commit()
        session.close()
        return render_template('newForm/formSubmitted.html', error=False)
    except BaseException as e:
        session.close()
        print("Error form submit: " + str(e))
        return render_template('newForm/formSubmitted.html', error=True)
