import json

from app.test.base_test_class import BaseTestClass


class AddResultTestCase(BaseTestClass):
    def get_a_valid_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        return message['questions'][0]

    def get_a_valid_user(self):
        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        return message[0]

    def test_add_result_if_valid_request_is_sent_for_success_then_both_question_counters_are_incremented(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        user_original = self.get_a_valid_user()
        question_original = self.get_a_valid_question()

        res = self.client().post('/results', json={
            'user_id': user_original['id'],
            'question_id': question_original['id'],
            'success': True})
        data = json.loads(res.data)

        res = self.client().get('/questions')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        for q in message['questions']:
            if q['id'] == question_original['id']:
                question_new = q
                break

        self.assertEqual(question_new['answer_count'], question_original['answer_count'] + 1)
        self.assertEqual(question_new['correct_answers'], question_original['correct_answers'] + 1)

    def test_add_result_if_valid_request_is_sent_for_success_then_only_question_attempt_counter_is_incremented(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        user_original = self.get_a_valid_user()
        question_original = self.get_a_valid_question()

        res = self.client().post('/results', json={
            'user_id': user_original['id'],
            'question_id': question_original['id'],
            'success': False})
        data = json.loads(res.data)

        res = self.client().get('/questions')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        for q in message['questions']:
            if q['id'] == question_original['id']:
                question_new = q
                break

        self.assertEqual(question_new['answer_count'], question_original['answer_count'] + 1)
        self.assertEqual(question_new['correct_answers'], question_original['correct_answers'])

    def test_add_result_if_valid_request_is_sent_for_success_then_both_user_counters_are_incremented(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        user_original = self.get_a_valid_user()
        question_original = self.get_a_valid_question()

        res = self.client().post('/results', json={
            'user_id': user_original['id'],
            'question_id': question_original['id'],
            'success': True})
        data = json.loads(res.data)

        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        for u in message:
            if u['id'] == question_original['id']:
                user_new = u
                break

        self.assertEqual(user_new['questions_answered'], user_original['questions_answered'] + 1)
        self.assertEqual(user_new['correct_answers'], user_original['correct_answers'] + 1)

    def test_add_result_if_valid_request_is_sent_for_success_then_only_user_attempt_counter_is_incremented(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        user_original = self.get_a_valid_user()
        question_original = self.get_a_valid_question()

        res = self.client().post('/results', json={
            'user_id': user_original['id'],
            'question_id': question_original['id'],
            'success': False})
        data = json.loads(res.data)

        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        for u in message:
            if u['id'] == question_original['id']:
                user_new = u
                break

        self.assertEqual(user_new['questions_answered'], user_original['questions_answered'] + 1)
        self.assertEqual(user_new['correct_answers'], user_original['correct_answers'])

    def test_add_result_if_user_id_is_neg1_then_no_user_counters_are_incremented(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        user_original = self.get_a_valid_user()
        question_original = self.get_a_valid_question()

        res = self.client().post('/results', json={
            'user_id': -1,
            'question_id': question_original['id'],
            'success': True})
        data = json.loads(res.data)

        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        for u in message:
            if u['id'] == question_original['id']:
                user_new = u
                break

        self.assertEqual(user_new['questions_answered'], user_original['questions_answered'])
        self.assertEqual(user_new['correct_answers'], user_original['correct_answers'])

    def test_add_result_if_parameter_user_id_is_missing_then_throws_422(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().post('/results', json={
            'question_id': self.get_a_valid_question()['id'],
            'success': True})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_add_result_if_parameter_question_id_is_missing_then_throws_422(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().post('/results', json={
            'user_id': self.get_a_valid_user()['id'],
            'success': True})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_add_result_if_parameter_success_is_missing_then_throws_422(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().post('/results', json={
            'user_id': self.get_a_valid_user()['id'],
            'question_id': self.get_a_valid_question()['id']})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_add_result_if_parameter_user_id_is_not_in_database_then_throws_422(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().post('/results', json={
            'user_id': -2,
            'question_id': self.get_a_valid_question()['id'],
            'success': True})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_add_result_if_parameter_question_id_is_not_in_database_then_throws_422(self):
        self.add_data_to_database([1, 2, 1])
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().post('/results', json={
            'user_id': self.get_a_valid_user()['id'],
            'question_id': -1,
            'success': True})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)
