import json

from app.test.base_test_class import BaseTestClass


class PlayTestCase(BaseTestClass):
    def test_play_with_invalid_category_returns_error404(self):
        res = self.client().post('/', json={
            'category': 'BadCategory'
        })
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_play_when_no_questions_to_ask_returns_error404(self):
        res = self.client().post('/', json={
        })
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 404)

    def test_play_when_request_is_valid_then_returns_a_question(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/', json={
        })
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue('question' in message)
        self.assertTrue('answer' in message)
        self.assertTrue('id' in message)
        self.assertTrue('category' in message)
        self.assertTrue('difficulty' in message)
