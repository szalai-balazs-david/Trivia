import json

from app.test.base_test_class import BaseTestClass


class GetQuestionsTestCase(BaseTestClass):
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

        self.assertEqual(1, message['question_count'])

    def test_get_questions_returns_10_questions_if_possible(self):
        self.add_data_to_database([15, 2, 1])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
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
