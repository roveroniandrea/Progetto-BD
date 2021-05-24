from flask import Blueprint
from flask_login import login_required
from pages.formPage.accessForm import accessForm
from pages.formPage.addFormAccess import getFormAccesses, addFormAccess
from pages.formPage.deleteForm import deleteForm
from pages.formPage.showFormStats import showFormStats
from pages.formPage.submitAnswer import submitAnswer

formPageBlueprint = Blueprint('formPage', __name__)


@formPageBlueprint.route('/q/<int:form_id>', methods=['GET'])
@login_required
def defAccessForm(form_id):
    return accessForm(form_id)


@formPageBlueprint.route('/q/<int:form_id>', methods=['POST'])
@login_required
def defSubmitAnswer(form_id):
    return submitAnswer(form_id)


@formPageBlueprint.route('/q/<int:form_id>/delete', methods=['POST'])
@login_required
def defDeleteForm(form_id):
    return deleteForm(form_id)


@formPageBlueprint.route('/q/<int:form_id>/stats', methods=['GET'])
@login_required
def defShowFormStats(form_id):
    return showFormStats(form_id)


@formPageBlueprint.route('/q/<int:form_id>/accesses', methods=['GET'])
@login_required
def defGetFormAccesses(form_id):
    return getFormAccesses(form_id)


@formPageBlueprint.route('/q/<int:form_id>/accesses/<string:email>', methods=['POST'])
@login_required
def defAddFormAccess(form_id, email):
    return addFormAccess(form_id, email)
