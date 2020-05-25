import json

from app.test.base_test_class import BaseTestClass


class SearchQuestionTestCase(BaseTestClass):
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
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_search_questions_if_page_request_too_high_then_throws_404(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions/search', json={
            'search_term': 'BadSearchTerm',
            'page': 1000
        })
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)
