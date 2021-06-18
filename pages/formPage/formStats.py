import csv
import io

from flask import abort, Response
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session
from lib.types.Question import QuestionTypeEnum
from lib.types.answers.Answer import Answer


def generateCSV(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        form = user.ownedFormsRel.filter_by(id=form_id).one()
        filename = form.title + ".csv"
        questions = []
        for question in form.questionsRel:
            question_entry = {
                'id': question.id,
                'question': question.question,
                'type': question.type
            }
            questions.append(question_entry)

        file = io.StringIO()
        writer = csv.writer(file)
        questions.sort(key=lambda q: q["id"])
        writer.writerow(map(lambda q: q["question"], questions))

        for access in form.accessesRel:
            answers = access.answersRel.order_by(Answer.question).all()
            answers_to_write = []

            index = 0
            for question in questions:
                if index < len(answers) and answers[index].question == question['id']:
                    if question['type'] == QuestionTypeEnum.text:
                        answers_to_write.append(answers[index].openAnswerRel.one().answer)
                    if question['type'] == QuestionTypeEnum.date:
                        answers_to_write.append(answers[index].dateAnswerRel.one().answer)
                    if question['type'] == QuestionTypeEnum.single:
                        answers_to_write.append(answers[index].singleAnswerRel.one().answer)
                    if question['type'] == QuestionTypeEnum.multi:
                        answers_to_write.append(', '.join(answers[index].multipleAnswerRel.one().answer))
                    index = index + 1
                else:
                    answers_to_write.append(' ')

            writer.writerow(answers_to_write)

        response = Response(file.getvalue(), mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename=filename)
        session.close()
        return response

    except SQLAlchemyError as e:
        print("Error generateCSV: " + str(e))
        session.close()
        return abort(401)
