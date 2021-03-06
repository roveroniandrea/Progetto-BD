import enum

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY, Enum
from sqlalchemy.orm import relationship

from lib.initDB import Base


class QuestionTypeEnum(enum.Enum):
    text = 1
    single = 2
    multi = 3
    date = 4

    def asString(self):
        """Used by the client to check which type has the question"""
        if self == QuestionTypeEnum.text:
            return 'text'
        if self == QuestionTypeEnum.single:
            return 'single'
        if self == QuestionTypeEnum.multi:
            return 'multi'
        if self == QuestionTypeEnum.date:
            return 'date'

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
    options = Column(ARRAY(String))
    form = Column(Integer, ForeignKey('forms.id'))

    formRel = relationship('Form', back_populates='questionsRel')
    """1:M relationship to the forms table"""

    answersRel = relationship('Answer', back_populates='questionRel', lazy='dynamic')
    """1:M relationship with answers table"""

    def __repr__(self):
        """Used to print the Question object"""
        return "Question: {id: '%s', question: '%s', required: '%s', type: '%s', options: '%s', form: '%s'}" % (
            self.id, self.question, self.required, self.type, self.options, self.form)
