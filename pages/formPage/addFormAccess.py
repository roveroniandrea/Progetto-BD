from flask import jsonify, Response
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import abort

from lib.initDB import Session
from lib.types.Access import Access


def getFormAccesses(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        form = user.ownedFormsRel.filter_by(id=form_id).one()
        return jsonify(list(map(lambda a: a.user, form.accessesRel.filter(Access.user != user.email).all())))

    except SQLAlchemyError:
        session.close()
        return abort(401)


def addFormAccess(form_id, email):
    session = Session()
    user = session.merge(current_user)
    try:
        form = user.ownedFormsRel.filter_by(id=form_id).one()
        access = Access()
        access.user = email
        access.formRel = form
        session.add(access)
        session.commit()
        session.close()
        return Response(200)

    except SQLAlchemyError:
        session.close()
        return abort(401)
