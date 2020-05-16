import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

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

            self.db.session.query(Question).delete()
            self.db.session.query(Category).delete()
            self.db.session.commit()
    
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

    def add_data_to_database(self, categories_and_questions):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            for i in range(len(categories_and_questions)):
                cat = Category("Category" + str(i+1))
                self.db.session.add(cat)
                self.db.session.commit()
                for j in range(categories_and_questions[i]):
                    question = Question("Question" + str(i) + "." + str(j), "Answer" + str(i) + "." + str(j), cat.id, 1)
                    self.db.session.add(question)
            self.db.session.commit()

    def test_get_categories_returns_list_of_categories(self):
        self.add_data_to_database([1, 2, 1])

        res = self.client().get('/categories')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue('Category1' in message)
        self.assertTrue('Category2' in message)
        self.assertTrue('Category3' in message)

    def test_get_questions_returns_list_of_categories(self):
        self.add_data_to_database([1, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)['categories']

        self.assertTrue('Category1' in message)
        self.assertTrue('Category2' in message)
        self.assertTrue('Category3' in message)

    def test_get_questions_if_category_is_provided_then_returns_current_category(self):
        self.add_data_to_database([1, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertEqual("Category1", message['current_category'])

    def test_get_questions_if_no_category_is_provided_returns_current_category_with_value_all(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertEqual('all', message['current_category'])

    def test_get_questions_returns_number_of_total_questions(self):
        self.add_data_to_database([1, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertEqual(4, message['question_count'])

    def test_get_questions_returns_10_questions_if_possible(self):
        self.add_data_to_database([15, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        print(message['questions'])
        self.assertEqual(10, len(message['questions']))

    def test_get_questions_returns_less_than_10_questions_on_last_page(self):
        self.add_data_to_database([15, 2, 1])

        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertEqual(8, len(message['questions']))

    def test_get_questions_with_category_returns_error404_if_page_request_is_out_of_bounds(self):
        res = self.client().get('/questions?category=Category1&page=1000')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_get_questions_without_category_returns_error404_if_page_request_is_out_of_bounds(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_get_questions_with_invalid_category_returns_error404(self):
        res = self.client().get('/questions?category=BadCategory')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_delete_question_with_invalid_id_returns_error404(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_delete_question_with_valid_id_removes_question_from_options(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        id = message['questions'][0]['id']

        res = self.client().delete('/questions/' + str(id))
        data = json.loads(res.data)
        message2 = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(id, message2['question']['id'])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message3 = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(message['question_count']-1, message3['question_count'])

    def test_create_question_if_valid_request_is_sent_then_new_question_is_added(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'answer': 'ans',
            'category': 'Category1',
            'difficulty': 1})
        data = json.loads(res.data)

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(9, message['question_count'])
        self.assertEqual('ans', message['questions'][5]['answer'])
        self.assertEqual('quest', message['questions'][5]['question'])
        self.assertEqual(1, message['questions'][5]['difficulty'])

    def test_create_question_if_question_not_in_request_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'answer': 'ans',
            'category': 'Category1',
            'difficulty': 1})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_question_if_answer_not_in_request_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'category': 'Category1',
            'difficulty': 1})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_question_if_category_not_in_request_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'answer': 'ans',
            'difficulty': 1})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_question_if_difficulty_not_in_request_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'answer': 'ans',
            'category': 'Category1'})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_question_if_nonexisting_category_is_provided_then_throws_404(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'answer': 'ans',
            'category': 'CategoryUnknown',
            'difficulty': 1})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_search_questions_if_search_term_not_in_request_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_search_questions_if_request_is_valid_then_response_is_correct(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions/search', json={
            'search_term': '1.1'
        })
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(1, message['question_count'])
        self.assertTrue('1.1' in message['questions'][0]['question'])

    def test_search_questions_if_request_is_valid_for_multiple_questions_then_response_is_limited_to_10(self):
        self.add_data_to_database([15, 2, 1])

        res = self.client().post('/questions/search', json={
            'search_term': '0.'
        })
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(10, len(message['questions']))

    def test_search_questions_if_no_question_match_the_search_term_then_throws_404(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions/search', json={
            'search_term': 'BadSearchTerm'
        })
        data = json.loads(res.data)
        print(data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_search_questions_if_page_request_too_high_then_throws_404(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions/search', json={
            'search_term': 'BadSearchTerm',
            'page': 1000
        })
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()