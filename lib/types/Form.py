from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from lib.initDB import Base


class Form(Base):
    """Type definition for the Forms table in DB"""
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    owner = Column(String, ForeignKey('users.email'))

    ownerUserRel = relationship('User', back_populates='ownedFormsRel')
    """1:M relationship to the users table"""
    questionsRel = relationship('Question', back_populates='formRel')
    """1:M relationship to the questions table"""

    def __repr__(self):
        """Used to print the Form object"""
        return "Form: {id: '%s', title: '%s', owner: '%s'}" % (self.id, self.title, self.owner)