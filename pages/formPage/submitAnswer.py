import json

from flask import request, render_template
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
    """Saves the answers to a form in the db. Checks if the user has access to the form"""
    session = Session()

    try:
        form = session.query(Form).filter_by(id=form_id).one()
        access = form.accessesRel.filter_by(user=current_user.email).one()
        if access.access_id is not None:
            raise Exception('User has already answered to this form')

        access.access_id = generateNextAccessId()

        for submitted_answer in json.loads(request.form['answers']):
            question = form.questionsRel.filter_by(id=submitted_answer['id']).one()
            answer = Answer()
            answer.accessRel = access
            answer.question = question.id

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
        return render_template('submit_status.html', error=False)
    except BaseException as e:
        session.close()
        print("Error submit answers: " + str(e))
        return render_template('error.html', error="Errore Submit delle risposte", description="C'è stato un errore nell'invio delle tue risposte. Riprova più tardi")
