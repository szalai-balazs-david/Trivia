import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def check_if_operation_was_successful_and_get_payload(self, data):
        self.assertTrue(data['success'])
        self.assertEqual(0, data['error'])
        return data['message']

    def check_if_operation_failed_with_error_code(self, data, expected_error_code):
        self.assertFalse(data['success'])
        self.assertEqual(expected_error_code, data['error'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_returns_list_of_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue('Science' in message)
        self.assertTrue('Art' in message)
        self.assertTrue('Geography' in message)
        self.assertTrue('History' in message)
        self.assertTrue('Entertainment' in message)
        self.assertTrue('Sports' in message)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()