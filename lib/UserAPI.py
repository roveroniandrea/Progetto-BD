import os
from hashlib import blake2b

from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session
from lib.types.User import User


def validateUser(email, password):
    """Returns the corrisponding user given its credentials, None if the user doesn't exist or the password does not
    match """
    session = Session()
    user = None
    try:
        user = session.query(User).filter_by(email=email).one()
    finally:
        session.close()
        if user:
            h = blake2b()
            h.update(user.salt)
            h.update(password.encode())
            if h.hexdigest() == user.digest:
                return user
        return None


def loadUser(email):
    """Loads an ALREADY AUTHENTICATED user from the DB"""
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user
    except SQLAlchemyError as e:
        session.close()
        print("Error loading user: " + str(e))
        return None


def registerUser(email, password):
    """Adds a new user to the DB, crypting its password. Returns the user on sucess, None otherwise"""
    h = blake2b()
    user = User()
    user.email = email
    user.salt = os.urandom(blake2b.SALT_SIZE)
    h.update(user.salt)
    h.update(password.encode())
    user.digest = h.hexdigest()
    session = Session()
    try:
        session.add(user)
        session.commit()
        session.close()
        return user
    except SQLAlchemyError as e:
        print("Error inserting " + email + " : " + str(e))
        session.close()
        return None
