from flask import render_template
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session


def accessForm(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        access = user.accessesRel.filter_by(form=form_id).one()
    except SQLAlchemyError:
        session.close()
        return render_template('error.html', error="Unauthorized", description="Potresti non avere i permessi per accedere a questa pagina")

    if access.access_id is None:
        # Risposta al questionario
        template = render_template("formPage/answerForm.html", form=access.formRel)
        session.close()
        return template
    else:
        # TODO: revisione questionario
        session.close()
        return "TODO revisione"
