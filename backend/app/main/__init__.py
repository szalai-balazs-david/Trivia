from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.main.config import config_by_name

db = SQLAlchemy()


def create_app(config_name):
    from app.main.models import Question, Category
    from app.main.controller import app as blueprint
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    app.register_blueprint(blueprint)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
