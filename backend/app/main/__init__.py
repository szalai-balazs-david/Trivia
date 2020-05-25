from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.main.config import config_by_name
from app.main.util.dto import get_response

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

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
