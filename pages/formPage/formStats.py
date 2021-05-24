import csv
import io

from flask import render_template, abort, Response
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session
from lib.types.Access import Access
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
            }

            questions.append(question_entry)

        file = io.StringIO()
        writer = csv.writer(file)
        questions.sort(key=lambda q: q["id"])
        writer.writerow(map(lambda q: q["question"], questions))

        for access in form.accessesRel:
            answers = access.answersRel.order_by(Answer.question).all()
            answers_to_write = []
            for answer in answers:
                print(answer)
                question = answer.questionRel.one()

                if question.type == QuestionTypeEnum.text:
                    answers_to_write.append(answer.openAnswerRel.one().answer)
                if question.type == QuestionTypeEnum.date:
                    answers_to_write.append(answer.dateAnswerRel.one().answer)
                if question.type == QuestionTypeEnum.single:
                    answers_to_write.append(answer.singleAnswerRel.one().answer)
                if question.type == QuestionTypeEnum.multi:
                    answers_to_write.append(answer.multipleAnswerRel.one().answer)

            writer.writerow(answers_to_write)

        response = Response(file.getvalue(), mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename=filename)
        return response

    except SQLAlchemyError as e:
        print("Error showFormStats: " + str(e))
        session.close()
        return abort(401)
