import json

from app.test.base_test_class import BaseTestClass


class DeleteQuestionTestCase(BaseTestClass):
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
        self.assertEqual(str(id), message2['question'])

        res = self.client().get('/questions?category=Category1')
        data = json.loads(res.data)
        message3 = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertEqual(message['question_count']-1, message3['question_count'])
