import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app.main.models import Question, Category
from app.main import create_app
from app.main import db


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db.create_all()
            db.session.commit()

            self.db.session.query(Question).delete()
            self.db.session.query(Category).delete()
            self.db.session.commit()

    def tearDown(self):
        pass

    def check_if_operation_was_successful_and_get_payload(self, data):
        self.assertTrue(data['success'])
        self.assertEqual(0, data['error'])
        return data['message']

    def check_if_operation_failed_with_error_code(self, data, expected_error_code):
        self.assertFalse(data['success'])
        self.assertEqual(expected_error_code, data['error'])

    def add_data_to_database(self, categories_and_questions):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            for i in range(len(categories_and_questions)):
                cat = Category()
                cat.type = "Category" + str(i+1)
                self.db.session.add(cat)
                self.db.session.commit()
                for j in range(categories_and_questions[i]):
                    question = Question()
                    question.question = "Question" + str(i) + "." + str(j)
                    question.answer = "Answer" + str(i) + "." + str(j)
                    question.category_id = cat.id
                    question.difficulty = 1
                    self.db.session.add(question)
            self.db.session.commit()
