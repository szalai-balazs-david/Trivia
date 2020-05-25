from app.main import db
from app.main.models import Question, Category
from app.main.util.dto import get_response
from flask_restplus import abort
import random


def create_new_question(question, answer, category, difficulty):
    q = Question.query.filter_by(question=question).first()
    if not q:
        new_question = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category
        )
        save_question(new_question)
        return True
        # original return
        # response_object = {
        #     'status': 'success',
        #     'message': 'Successfully registered.'
        # }
        # return response_object, 201
    else:
        return False
        # original return
        # response_object = {
        #     'status': 'fail',
        #     'message': 'User already exists. Please Log in.',
        # }
        # return response_object, 409


def get_random_question(used_questions=None, category='all'):
    if used_questions is None:
        used_questions = []
    if category == 'all':
        questions = Question.query.filter(~Question.id.in_(used_questions)).all()
    else:
        cat_id = Category.query.filter(Category.type == category).first().id
        questions = Question.query.filter(Question.category_id == cat_id) \
            .filter(~Question.id.in_(used_questions)).all()
    if len(questions) <= 0:
        abort(422)
    return get_response(random.choice(questions))# {'data': random.choice(questions)}


def delete(data):
    db.session.delete(data)
    db.session.commit()


def save_question(data):
    db.session.add(data)
    db.session.commit()
