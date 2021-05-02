from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session

formPageBlueprint = Blueprint('formPage', __name__)


@formPageBlueprint.route('/q/<int:form_id>', methods=['GET'])
@login_required
def accessForm(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        access = user.accessesRel.filter_by(form=form_id).one()
    except SQLAlchemyError:
        session.close()
        return "Non autorizzato"

    if access.access_id is None:
        # Risposta al questionario
        template = render_template("formPage/answerForm.html", form=access.formRel)
        session.close()
        return template
    else:
        # TODO: revisione questionario
        session.close()
        return "TODO revisione"


@formPageBlueprint.route('/q/<int:form_id>', methods=['POST'])
@login_required
def submitAnswer(form_id):
    # TODO: submit risposte
    return "TODO: submit"
