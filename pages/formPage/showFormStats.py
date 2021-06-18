from flask import render_template, abort
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session
from lib.types.Access import Access
from lib.types.Question import QuestionTypeEnum


def showFormStats(form_id):
    """Returns the stats of a form. Only if the user is the owner"""
    session = Session()
    user = session.merge(current_user)
    try:
        form = user.ownedFormsRel.filter_by(id=form_id).one()
        total_accesses = form.accessesRel.count()
        answered_accesses = form.accessesRel.filter(Access.access_id.isnot(None)).count()

        questions = []
        for question in form.questionsRel:
            question_entry = {
                'type': question.type.asString(),
                'question': question.question,
                'options': question.options,
                'openAnswers': [],
                'optionsAnswers': {},
                'notAnswered': answered_accesses - question.answersRel.count()
            }
            if question.type == QuestionTypeEnum.text:
                question_entry['openAnswers'] = list(map(lambda a: a.openAnswerRel.one().answer, question.answersRel.all()))
            if question.type == QuestionTypeEnum.date:
                question_entry['openAnswers'] = list(map(lambda a: a.dateAnswerRel.one().answer, question.answersRel.all()))
            if question.type == QuestionTypeEnum.single:
                for opt in question.options:
                    question_entry['optionsAnswers'][opt] = len(
                        list(filter(lambda a: a.singleAnswerRel.one().answer == opt, question.answersRel.all())))
            if question.type == QuestionTypeEnum.multi:
                for opt in question.options:
                    question_entry['optionsAnswers'][opt] = len(
                        list(filter(lambda a: opt in a.multipleAnswerRel.one().answer, question.answersRel.all())))

            questions.append(question_entry)

        return render_template("formPage/formStats.html", total_accesses=total_accesses,
                               answered_accesses=answered_accesses, questions=questions, form=form)

    except SQLAlchemyError as e:
        print("Error showFormStats: " + str(e))
        session.close()
        return abort(401)
