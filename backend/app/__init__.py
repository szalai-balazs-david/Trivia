from flask_restplus import Api
from flask import Blueprint

from .main.controller.question_controller import api as question_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='TITLE',
          version='1.0',
          description='Description'
          )

api.add_namespace(question_ns, path='/play')