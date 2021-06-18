from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from lib.initDB import Base


class SingleAnswer(Base):
    """Type definition for the single_answers table in DB"""
    __tablename__ = 'single_answers'

    id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
    answer = Column(String)

    answerRel = relationship('Answer', back_populates='singleAnswerRel')
    """1:1 relationship with answers table"""

    def __repr__(self):
        """Used to print the SingleAnswer object"""
        return "SingleAnswer: {id: '%s', answer: '%s'}" % (self.id, self.answer)
