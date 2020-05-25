from app.main import db
from app.main.models import Question, Category
from app.main.util import get_response
from flask import abort, jsonify
import random


def get_categories_as_list():
    data = []
    for cat in Category.query.all():
        data.append(cat.type)
    return data


def get_categories():
    return get_response(get_categories_as_list())


def serialize_question(question):
    return {
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'difficulty': question.difficulty,
        'category': question.cat.type,
    }


def serialize_questions(question):
    data = []
    for q in question:
        data.append(serialize_question(q))
    return data


def verify_category_exists(category):
    if Category.query.filter(Category.type == category).count() != 1:
        abort(404)


def get_questions(page, category):
    if category == 'all':
        questions = Question.query.all()
    else:
        # ToDo: Check if I can optimize this
        if Category.query.filter(Category.type == category).count() == 0:
            abort(404)
        category_id = Category.query.filter(Category.type == category).first().id
        questions = Question.query.filter(Question.category_id == category_id).all()

    questions_per_page = 10
    first_question_index = (page - 1) * questions_per_page
    if len(questions) < first_question_index:
        abort(404)

    return get_response({
        'current_category': category,
        'categories': get_categories_as_list(),
        'question_count': len(questions),
        'questions': serialize_questions(questions[first_question_index:(first_question_index + questions_per_page)])
    })


def delete_question(question_id):
    q = Question.query.get(question_id)

    if q is None:
        abort(404)
    delete(q)

    return get_response({
        'question': question_id
    })


def create_new_question(question, answer, category, difficulty):
    verify_category_exists(category)

    cat_id = Category.query.filter(Category.type == category).first().id

    new_question = Question()
    new_question.question = question
    new_question.answer = answer
    new_question.category_id = cat_id
    new_question.difficulty = difficulty
    save(new_question)

    return get_response({
        'question': serialize_question(new_question)
    })


def search_for_question(search_term, page):
    questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()

    questions_per_page = 10
    first_question_index = (page - 1) * questions_per_page
    if len(questions) <= first_question_index:
        abort(404)

    return get_response({
        'question_count': len(questions),
        'questions': serialize_questions(questions[first_question_index:(first_question_index + questions_per_page)])
    })


def get_random_question(used_questions, category):
    if category == 'all':
        questions = Question.query.filter(~Question.id.in_(used_questions)).all()
    else:
        verify_category_exists(category)
        cat_id = Category.query.filter(Category.type == category).first().id
        questions = Question.query.filter(Question.category_id == cat_id) \
            .filter(~Question.id.in_(used_questions)).all()

    if len(questions) <= 0:
        abort(404, 'No suitable question found')

    return get_response(serialize_question(random.choice(questions)))


def delete(data):
    db.session.delete(data)
    db.session.commit()


def save(data):
    db.session.add(data)
    db.session.commit()

