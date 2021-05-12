from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from lib.initDB import Base


class Answer(Base):
    """Type definition for the answers table in DB"""
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    access = Column(Integer, ForeignKey('accesses.access_id'))
    question = Column(Integer, ForeignKey('questions.id'))

    accessRel = relationship('Access', back_populates='answersRel')
    """1:M relationship with accesses table"""

    questionRel = relationship('Question', back_populates='answersRel')
    """1:M relationship with questions table"""

    openAnswerRel = relationship('OpenAnswer', back_populates='answerRel', cascade="all, delete-orphan", lazy="joined")
    """1:1 relationship with open_answers table"""

    singleAnswerRel = relationship('SingleAnswer', back_populates='answerRel', cascade="all, delete-orphan", lazy="joined")
    """1:1 relationship with single_answers table"""

    multipleAnswerRel = relationship('MultipleAnswer', back_populates='answerRel', cascade="all, delete-orphan", lazy="joined")
    """1:1 relationship with multiple_answers table"""

    dateAnswerRel = relationship('DateAnswer', back_populates='answerRel', cascade="all, delete-orphan", lazy="joined")
    """1:1 relationship with date_answers table"""

    def __repr__(self):
        """Used to print the Answer object"""
        return "Anser: {id: '%s', access: '%s', question: '%s'}" % (self.id, self.access, self.question)
