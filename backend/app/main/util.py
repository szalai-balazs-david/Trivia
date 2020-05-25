from flask import jsonify
from app.main.models import Question, Category


def get_response(data, success=True, error=0):
    return jsonify({
        "success": success,
        "error": error,
        "message": data
    })
