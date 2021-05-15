from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from lib.initDB import Session
from lib.types.Access import generateNextAccessId, Access
from lib.types.Form import Form
from lib.types.Question import QuestionTypeEnum
from lib.types.answers.Answer import Answer
from lib.types.answers.DateAnswer import DateAnswer
from lib.types.answers.MultipleAnswer import MultipleAnswer
from lib.types.answers.OpenAnswer import OpenAnswer
from lib.types.answers.SingleAnswer import SingleAnswer

formPageBlueprint = Blueprint('formPage', __name__)


@formPageBlueprint.route('/q/<int:form_id>', methods=['GET'])
@login_required
def accessForm(form_id):
    session = Session()
    user = session.merge(current_user)
    try:
        access = user.accessesRel.filter_by(form=form_id).one()
    except SQLAlchemyError:
        session.close()
        return "Non autorizzato"

    if access.access_id is None:
        # Risposta al questionario
        template = render_template("formPage/answerForm.html", form=access.formRel)
        session.close()
        return template
    else:
        # TODO: revisione questionario
        session.close()
        return "TODO revisione"


@formPageBlueprint.route('/q/<int:form_id>', methods=['POST'])
@login_required
def submitAnswer(form_id):
    session = Session()

    # request.form = json.loads(
    #    "{\"answers\":[{\"id\":4,\"type\":\"text\",\"answer\":\"lorem ipsum\"},{\"id\":3,\"type\":\"single\",\"answer\":\"Opt1\"}]}")

    try:
        form = session.query(Form).filter_by(id=form_id).one()
        access = form.accessesRel.filter_by(user=current_user.email).one()
        access.access_id = generateNextAccessId()

        for submitted_answer in request.form['answers']:
            question = form.questionsRel.filter_by(id=submitted_answer['id']).one()
            answer = Answer()
            answer.accessRel = access
            answer.questionRel = question
            answer_type = submitted_answer['type']

            if answer_type == 'text':
                typed_answer = OpenAnswer()
            elif answer_type == 'single':
                typed_answer = SingleAnswer()
            elif answer_type == 'multi':
                typed_answer = MultipleAnswer()
            elif answer_type == 'date':
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


@formPageBlueprint.route('/q/<int:form_id>/delete', methods=['POST'])
@login_required
def deleteForm(form_id):
    session = Session()
    try:
        form = session.query(Form).filter_by(id=form_id).one()
        if form.owner == current_user.email:
            accesses = form.accessesRel.all()
            for acc in accesses:
                if acc.access_id:
                    answers = acc.answersRel.all()
                    for answer in answers:
                        answer.openAnswerRel = []
                        answer.dateAnswerRel = []
                        answer.multipleAnswerRel = []
                        answer.singleAnswerRel = []

                    acc.answersRel.delete()

            form.accessesRel.delete()
            form.questionsRel.delete()
            session.delete(form)

            session.commit()
            session.close()
            # print("form deleted")
            return redirect('/')
        else:
            session.close()
            return "Unauthorized Access"
    except SQLAlchemyError as e:
        session.close()
        print("Error DELETE: " + str(e))
        return "errore cancellazione"


@formPageBlueprint.route('/q/<int:form_id>/stats', methods=['GET'])
@login_required
def showFormStats(form_id):
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
                question_entry['openAnswers'] = map(lambda q: q.openAnswerRel.one().answer, question.answersRel.all())
            if question.type == QuestionTypeEnum.date:
                question_entry['openAnswers'] = map(lambda q: q.dateAnswerRel.one().answer, question.answersRel.all())
            if question.type == QuestionTypeEnum.single:
                for opt in question.options:
                    question_entry['optionsAnswers'][opt] = len(list(filter(lambda q: q.singleAnswerRel.one().answer == opt, question.answersRel.all())))
            if question.type == QuestionTypeEnum.multi:
                for opt in question.options:
                    question_entry['optionsAnswers'][opt] = len(list(filter(lambda q: q.singleAnswerRel.one().answer.contains(opt), question.answersRel.all())))

            questions.append(question_entry)

        return render_template("formPage/formStats.html", total_accesses=total_accesses,
                               answered_accesses=answered_accesses, questions = questions)

    except SQLAlchemyError as e:
        print("Error showFormStats: " + str(e))
        session.close()
        return "Non autorizzato"
