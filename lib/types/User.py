from flask_login import UserMixin
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import relationship

from lib.initDB import Base


class User(UserMixin, Base):
    """Type definition of the Users table in DB"""
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    salt = Column(LargeBinary)
    digest = Column(String)

    ownedFormsRel = relationship("Form", back_populates="ownerUserRel")
    """1:M relationship to the forms table"""

    accessesRel = relationship('Access', back_populates='userRel', lazy='dynamic')
    """1:M relationship with accesses table"""

    def get_id(self):
        """Used by flask_login to identify the user. Returns the email aka the Primary Key"""
        return self.email

    def __repr__(self):
        """Used to print the User object"""
        return "User: {email: '%s'}" % self.email
