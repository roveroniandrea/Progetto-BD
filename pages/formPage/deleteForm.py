from flask import render_template, abort
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import redirect

from lib.initDB import Session
from lib.types.Form import Form


def deleteForm(form_id):
    session = Session()
    try:
        form = session.query(Form).filter_by(id=form_id).one()
        if form.owner == current_user.email:
            accesses = form.accessesRel.all()
            for acc in accesses:
                if acc.access_id:
                    answers = acc.answersRel.all()
                    for answer in answers:
                        answer.openAnswerRel = []
                        answer.dateAnswerRel = []
                        answer.multipleAnswerRel = []
                        answer.singleAnswerRel = []

                    acc.answersRel.delete()

            form.accessesRel.delete()
            form.questionsRel.delete()
            session.delete(form)

            session.commit()
            session.close()
            return redirect('/')
        else:
            session.close()
            return abort(401)
    except SQLAlchemyError as e:
        session.close()
        print("Error DELETE: " + str(e))
        return render_template('error.html', error="Errore cancellazione del form", description="C'è stato un errore nella cancellazione del form. Riprova più tardi")