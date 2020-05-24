from flask_restplus import Namespace, fields


class QuestionDto:
    api = Namespace('questions', description='operations related to questions')
    question = api.model('questions', {
        'public_id': fields.String(description='question identifier'),
        'question': fields.String(required=True, description='trivia question'),
        'answer': fields.String(required=True, description='trivia answer'),
        'category': fields.String(required=True, description='question category'),
        'difficulty': fields.String(required=True, description='question difficulty')
    })


class PlayDto:
    api = Namespace('play', description='operations related to questions')
    play_request = api.model('play', {
        'category': fields.String(default='all', description='category of the game'),
        'previous_questions': fields.List(fields.Integer, default=[], description='questions already asked')
    })
    play_result = api.model('questions', {
        'public_id': fields.Integer(required=True, attribute=lambda x: x.id, description='question identifier'),
        'question': fields.String(required=True, description='trivia question'),
        'answer': fields.String(required=True, description='trivia answer'),
        'category': fields.String(required=True, description='question category'),
        'difficulty': fields.String(required=True, description='question difficulty')
    })


class CategoryDto:
    api = Namespace('categories', description='operations related to categories')
    question = api.model('categories', {
        'public_id': fields.String(description='category Identifier'),
        'type': fields.String(required=True, description='category name')
    })