from flask_login import UserMixin
from sqlalchemy import Column, String, LargeBinary

from lib.initDB import Base


class User(UserMixin, Base):
    """Type definition of the Users table in DB"""
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    salt = Column(LargeBinary)
    digest = Column(String)

    def get_id(self):
        """Used by flask_login to identify the user. Returns the email aka the Primary Key"""
        return self.email

    def __repr__(self):
        """Used to print the User object"""
        return "<User(email='%s')>" % self.email
