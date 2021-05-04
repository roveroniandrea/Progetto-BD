from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from lib.initDB import Base


class OpenAnswer(Base):
    """Type definition for the open_answers table in DB"""
    __tablename__ = 'open_answers'

    id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
    answer = Column(String)

    answerRel = relationship('Answer', back_populates='openAnswerRel')
    """1:1 relationship with answers table"""

    def __repr__(self):
        """Used to print the OpenAnswer object"""
        return "OpenAnswer: {id: '%s', answer: '%s'}" % (self.id, self.answer)
