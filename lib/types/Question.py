import enum

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY, Enum
from sqlalchemy.orm import relationship

from lib.initDB import Base


class QuestionTypeEnum(enum.Enum):
    text = 1
    single = 2
    multi = 3
    date = 4

    def __repr__(self):
        """Used to print the QuestionTypeEnum class"""
        return "QuestionTypeEnum"


class Question(Base):
    """Type definition of the Questions table in DB"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    required = Column(Boolean)
    type = Column(Enum(QuestionTypeEnum), default=QuestionTypeEnum.text)
    option = Column(ARRAY(String))
    form = Column(Integer, ForeignKey('forms.id'))

    formRel = relationship('Form', back_populates='questionsRel')
    """1:M relationship to the forms table"""

    def __repr__(self):
        """Used to print the Question object"""
        return "Question: {id: '%s', question: '%s', required: '%s', type: '%s', option: '%s', form: '%s'}" % (self.id, self.question, self.required, self.type, self.option, self.form)
