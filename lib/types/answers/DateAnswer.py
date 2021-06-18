from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from lib.initDB import Base


class DateAnswer(Base):
    """Type definition for the date_answers table in DB"""
    __tablename__ = 'date_answers'

    id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
    answer = Column(Date)

    answerRel = relationship('Answer', back_populates='dateAnswerRel')
    """1:1 relationship with answer table"""

    def __repr__(self):
        """Used to print the DateAnswer object"""
        return "DateAnswer: {id: '%s', answer: '%s'}" % (self.id, self.answer)
