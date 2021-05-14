from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from lib.initDB import Base

class Form(Base):
    """Type definition for the Forms table in DB"""
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    owner = Column(String, ForeignKey('users.email'))
    color = Column(String)

    ownerUserRel = relationship('User', back_populates='ownedFormsRel')
    """1:M relationship to the users table"""
    questionsRel = relationship('Question', back_populates='formRel', lazy='dynamic')
    """1:M relationship to the questions table"""

    accessesRel = relationship('Access', back_populates='formRel', lazy='dynamic', cascade="all, delete-orphan")
    """1:M relationship with accesses table"""

    def __repr__(self):
        """Used to print the Form object"""
        return "Form: {id: '%s', title: '%s', owner: '%s' color: '%s'}" % (self.id, self.title, self.owner, self.color)
