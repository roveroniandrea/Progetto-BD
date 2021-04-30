from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY
from sqlalchemy.orm import relationship

from lib.initDB import Base


class QuestionTypeEnum(Enum):
    text = 1
    single = 2
    multi = 3
    date = 4


class Question(Base):
    """Type definition of the Questions table in DB"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    required = Column(Boolean)
    type = Column(Enum(QuestionTypeEnum))
    option = Column(ARRAY(String))
    form = Column(Integer, ForeignKey('forms.id'))

    formRel = relationship('Form', back_populates='questionsRel')
    """1:M relationship to the forms table"""
