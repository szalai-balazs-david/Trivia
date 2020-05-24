from app.main import db
from app.main.model.Question import Question
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


def get_random_question(used_questions=[], category='all'):
    if category == 'all':
        questions = Question.query.filter_by(Question.id not in used_questions).all()
    else:
        questions = Question.query.filter_by(Question.category == category)\
            .filter_by(Question.id not in used_questions).all()
    if len(questions) <= 0:
        # TODO: Handle this
        pass
    return random.choice(questions)


def delete(data):
    db.session.delete(data)
    db.session.commit()


def save_question(data):
    db.session.add(data)
    db.session.commit()
