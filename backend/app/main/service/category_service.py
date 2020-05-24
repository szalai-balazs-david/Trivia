from app.main import db
from app.main.models import Category


def create_new_category(name):
    c = Category.query.filter_by(type=name).first()
    if not c:
        new_category = Category(
            type=name
        )
        save_category(new_category)
        return True
        # original return
        # response_object = {
        #     'status': 'success',
        #     'message': 'Successfully registered.'
        # }
        # return response_object, 201
    else:
        return False
        # original return
        # response_object = {
        #     'status': 'fail',
        #     'message': 'User already exists. Please Log in.',
        # }
        # return response_object, 409


def save_category(data):
    db.session.add(data)
    db.session.commit()

