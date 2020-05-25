from flask import request, abort, Blueprint

from app.main.util import get_response
from app.main.service import \
    get_categories, \
    get_random_question, \
    get_questions, \
    delete_question, \
    create_new_question, \
    search_for_question


app = Blueprint('default', __name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.route('/categories', methods=['GET'])
def app_get_categories():
    return get_categories()


@app.route('/questions', methods=['GET'])
def app_get_questions():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all', type=str)

    return get_questions(page, category)


@app.route('/questions/<question_id>', methods=['DELETE'])
def app_delete_question(question_id):
    return delete_question(question_id)


@app.route('/questions', methods=['POST'])
def app_create_question():
    data = request.json
    if 'question' not in data:
        abort(422)
    if 'answer' not in data:
        abort(422)
    if 'category' not in data:
        abort(422)
    if 'difficulty' not in data:
        abort(422)

    return create_new_question(data['question'], data['answer'], data['category'], data['difficulty'])


@app.route('/questions/search', methods=['POST'])
def app_search_questions():
    data = request.json
    if 'search_term' not in data:
        abort(422)

    search_term = data['search_term']
    if 'page' not in data:
        page = 1
    else:
        page = data['page']

    return search_for_question(search_term, page)


@app.route('/', methods=['POST'])
def app_play():
    data = request.json

    if 'previous_questions' not in data:
        previous_questions = []
    else:
        previous_questions = data['previous_questions']

    if 'category' not in data:
        category = 'all'
    else:
        category = data['category']

    return get_random_question(previous_questions, category)


@app.errorhandler(404)
def not_found(error):
    return get_response("Not found: " + error.description, False, 404), 404


@app.errorhandler(422)
def unprocessable(error):
    return get_response("Unprocessable: " + error.description, False, 422), 422


@app.errorhandler(501)
def not_implemented(error):
    return get_response("Not Implemented: " + error.description, False, 501), 501
