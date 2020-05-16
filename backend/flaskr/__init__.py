import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, 'postgresql://localhost:5432/trivia')
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    Balazs: Is this what they want???
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def get_response(message, success=True, error=0):
        return jsonify({
            "success": success,
            "error": error,
            "message": message
        })

    def get_categories_method():
        data = []
        for cat in Category.query.all():
            data.append(cat.type)
        return data

    def get_questions_method(questions):
        data = []
        for q in questions:
            data.append(q.format())
        return data

    @app.route('/categories', methods=['GET'])
    def get_categories():
        return get_response(get_categories_method())

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', 'all', type=str)

        if (category == 'all'):
            questions = Question.query.all()
        else:
            if (Category.query.filter(Category.type == category).count() == 0):
                abort(404)
            category_id = Category.query.filter(Category.type == category).first().id
            questions = Question.query.filter(Question.category == category_id).all()

        questions_per_page = 10
        first_question_index = (page - 1) * questions_per_page
        if (len(questions) < first_question_index):
            abort(404)

        return get_response({
            'current_category': category,
            'categories': get_categories_method(),
            'question_count': Question.query.count(),
            'questions': get_questions_method(
                questions[first_question_index:(first_question_index + questions_per_page)])
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        q = Question.query.get(question_id)

        if q is None:
            abort(404)
        q.delete()

        return get_response({
            'question': q.format()
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.json
        if 'question' not in data:
            abort(422)
        if 'answer' not in data:
            abort(422)
        if 'category' not in data:
            abort(422)
        if 'difficulty' not in data:
            abort(422)
        if Category.query.filter(Category.type==data['category']).count() != 1:
            abort(404)

        cat_id = Category.query.filter(Category.type==data['category']).all()[0].id
        q = Question(data['question'], data['answer'], cat_id, data['difficulty'])
        q.insert()
        return get_response({
            'question': q.format()
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.json
        if 'search_term' not in data:
            abort(422)

        search_term = data['search_term']
        if 'page' not in data:
            page = 1
        else:
            page = data['page']


        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()

        questions_per_page = 10
        first_question_index = (page - 1) * questions_per_page
        if (len(questions) <= first_question_index):
            abort(404)

        return get_response({
            'question_count': len(questions),
            'questions': get_questions_method(
                questions[first_question_index:(first_question_index + questions_per_page)])
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/questions/<category_ID>', methods=['GET'])
    def get_questions_in_category(category_ID):
        abort(501)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/', methods=['POST'])
    def ask_question():
        abort(501)

    @app.errorhandler(404)
    def not_found(error):
        return get_response("Not found", False, 404), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return get_response("Unprocessable", False, 422), 422

    @app.errorhandler(501)
    def not_implemented(error):
        return get_response("Not Implemented", False, 501), 501

    return app
