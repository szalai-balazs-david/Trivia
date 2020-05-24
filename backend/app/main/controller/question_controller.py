from flask import request
from flask_restplus import Resource

from app.main.util.dto import PlayDto
from app.main.service.question_service import create_new_question, delete, get_random_question

api = PlayDto.api
_request = PlayDto.play_request
_result = PlayDto.play_result


@api.route('/')
class Play(Resource):
    @api.response(200, 'Success.')
    @api.doc('get a question to play trivia')
    @api.expect(_request, validate=True)
    @api.marshal_with(_result)
    def post(self):
        data = request.json
        return get_random_question(data['previous_questions'], data['category'])
