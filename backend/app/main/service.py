from app.main import db
from app.main.models import Question, Category, User
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


def serialize_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'questions_answered': user.questions_total,
        'correct_answers': user.questions_won
    }


def get_users():
    data = []
    for user in User.query.all():
        data.append(serialize_user(user))
    return get_response(data)


def serialize_question(question):
    return {
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'difficulty': question.difficulty,
        'category': question.cat.type,
        'answer_count': question.answer_attempt_count,
        'correct_answers': question.answer_success_count
    }


def serialize_questions(question):
    data = []
    for q in question:
        data.append(serialize_question(q))
    return data


def verify_category_exists(category):
    if Category.query.filter(Category.type == category).count() != 1:
        abort(404)


def verify_category_does_not_exists(category):
    if Category.query.filter(Category.type == category).count() > 0:
        abort(422)


def verify_user_does_not_exist(name):
    if User.query.filter(User.name == name).count() > 0:
        abort(422)


def verify_question_id_exists(question_id):
    if Question.query.filter(Question.id == question_id).count() != 1:
        abort(422)


def verify_user_id_exist_or_neg1(user_id):
    if User.query.filter(User.id == user_id).count() != 1 and user_id != -1:
        abort(422)


def get_questions(page, category):
    if category == 'all':
        questions = Question.query.all()
    else:
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
    if difficulty not in [1, 2, 3, 4, 5]:
        abort(422, "difficulty must be an integer between 1-5")

    cat_id = Category.query.filter(Category.type == category).first().id

    new_question = Question()
    new_question.question = question
    new_question.answer = answer
    new_question.category_id = cat_id
    new_question.difficulty = difficulty
    new_question.answer_success_count = 0
    new_question.answer_attempt_count = 0
    save(new_question)

    return get_response({
        'question': serialize_question(new_question)
    })


def add_result(user_id, question_id, success):
    print(str(user_id) + ", " + str(question_id) + ", " + str(success))
    verify_user_id_exist_or_neg1(user_id)
    verify_question_id_exists(question_id)

    question = Question.query.filter(Question.id == question_id).first()
    question.answer_attempt_count = Question.answer_attempt_count + 1
    if success:
        question.answer_success_count = Question.answer_success_count + 1

    if user_id != -1:
        user = User.query.filter(User.id == user_id).first()
        user.questions_total = User.questions_total + 1
        if success:
            user.questions_won = User.questions_won + 1
        user_info = serialize_user(user)
    else:
        user_info = 'None'

    db.session.commit()

    return get_response({
        'user': user_info,
        'question': serialize_question(question)
    })


def create_new_category(name):
    verify_category_does_not_exists(name)

    new_category = Category()
    new_category.type = name
    save(new_category)

    return get_response({
        'category': name
    })


def create_new_user(name):
    verify_user_does_not_exist(name)

    new_user = User()
    new_user.name = name
    new_user.questions_total = 0
    new_user.questions_won = 0
    save(new_user)

    return get_response({
        'name': name
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
