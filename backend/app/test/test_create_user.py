import json

from app.test.base_test_class import BaseTestClass


class CreateUserTestCase(BaseTestClass):
    def test_create_user_if_valid_request_is_sent_then_new_user_is_added(self):
        res = self.client().post('/users', json={
            'name': 'NewUser'})
        data = json.loads(res.data)

        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        found = False
        for user in message:
            if user['name'] == 'NewUser':
                found = True
                break
        self.assertTrue(found)

    def test_create_user_if_parameter_name_is_missing_then_throws_422(self):
        res = self.client().post('/users', json={})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_user_if_category_already_exists_then_throws_422(self):
        self.add_user_to_database([{
            'name': 'User1',
            'wins': 2,
            'answers': 5
        }])

        res = self.client().post('/users', json={
            'name': 'User1'})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)
