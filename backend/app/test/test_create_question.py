import json

from app.test.base_test_class import BaseTestClass


class CreateQuestionTestCase(BaseTestClass):
    def test_create_question_if_valid_request_is_sent_then_new_question_is_added(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/questions', json={
            'question': 'quest',
            'answer': 'ans',
            'category': 'Category1',
            'difficulty': "1"})
        data = json.loads(res.data)

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(6, message['question_count'])
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
