from flask_restplus import Api
from flask import Blueprint

from app.main.controller.question_controller import api as question_ns
from app.main.util.dto import get_response
from werkzeug import exceptions

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Trivia API.',
          version='1.0',
          description='2nd deliverable for Udacity FullStack Developer Nanodegree program.'
          )

api.add_namespace(question_ns, path='/play')


@api.errorhandler(exceptions.NotFound)
def not_found(error):
    return get_response("Not found", False, 404), 404


@api.errorhandler(exceptions.UnprocessableEntity)
def unprocessable(error):
    return get_response("Unprocessable", False, 422), 422


@api.errorhandler(exceptions.NotImplemented)
def not_implemented(error):
    return get_response("Not Implemented", False, 501), 501