from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session

formPageBlueprint = Blueprint('formPage', __name__)


@formPageBlueprint.route('/q/<int:form_id>', methods=['GET'])
@login_required
def newForm(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        access = user.accessesRel.filter_by(form=form_id).one()
    except SQLAlchemyError:
        return "Non autorizzato"

    if access.access_id is None:
        return "OK"
    else:
        # TODO: revisione questionario
        return "TODO revisione"
