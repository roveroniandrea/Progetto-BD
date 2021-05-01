from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session


def getUserForms(user):
    """Retrieves all the forms created by this user"""
    session = Session()
    query_user = user
    res = None
    if inspect(user).detached:
        query_user = session.merge(user)

    try:
        res = query_user.ownedFormsRel
    except SQLAlchemyError as e:
        print("Error retreving user's forms: " + str(e))
    finally:
        session.close()
        return res

