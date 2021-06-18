from sqlalchemy import Column, Integer, ForeignKey, String, ARRAY
from sqlalchemy.orm import relationship

from lib.initDB import Base


class MultipleAnswer(Base):
    """Type definition for the multiple_answers table in DB"""
    __tablename__ = 'multiple_answers'

    id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
    answer = Column(ARRAY(String))

    answerRel = relationship('Answer', back_populates='multipleAnswerRel')
    """1:1 relationship with answers table"""

    def __repr__(self):
        """Used to print the MultipleAnswer object"""
        return "MultipleAnswer: {id: '%s', answer: '%s'}" % (self.id, self.answer)
