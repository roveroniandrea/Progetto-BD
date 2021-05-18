import json

from flask import request
from flask_login import current_user

from lib.initDB import Session
from lib.types.Access import generateNextAccessId
from lib.types.Form import Form
from lib.types.Question import QuestionTypeEnum
from lib.types.answers.Answer import Answer
from lib.types.answers.DateAnswer import DateAnswer
from lib.types.answers.MultipleAnswer import MultipleAnswer
from lib.types.answers.OpenAnswer import OpenAnswer
from lib.types.answers.SingleAnswer import SingleAnswer


def submitAnswer(form_id):
    session = Session()

    try:
        form = session.query(Form).filter_by(id=form_id).one()
        access = form.accessesRel.filter_by(user=current_user.email).one()
        access.access_id = generateNextAccessId()

        for submitted_answer in json.loads(request.form['answers']):
            question = form.questionsRel.filter_by(id=submitted_answer['id']).one()
            answer = Answer()
            answer.accessRel = access
            answer.questionRel = question

            if question.type == QuestionTypeEnum.text:
                typed_answer = OpenAnswer()
            elif question.type == QuestionTypeEnum.single:
                typed_answer = SingleAnswer()
            elif question.type == QuestionTypeEnum.multi:
                typed_answer = MultipleAnswer()
            elif question.type == QuestionTypeEnum.date:
                typed_answer = DateAnswer()
            else:
                raise Exception('Answer type not valid')

            typed_answer.answerRel = answer
            typed_answer.answer = submitted_answer['answer']

        session.commit()
        session.close()
        return "Risposte salvate"
    except BaseException as e:
        session.close()
        print("Error submit answers: " + str(e))
        return "Errore submit"