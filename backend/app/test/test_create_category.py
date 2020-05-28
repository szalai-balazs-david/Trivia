import json

from app.test.base_test_class import BaseTestClass


class CreateCategoryTestCase(BaseTestClass):
    def test_create_category_if_valid_request_is_sent_then_new_category_is_added(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/categories', json={
            'name': 'NewCategory'})
        data = json.loads(res.data)

        res = self.client().get('/categories')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)
        self.assertTrue('NewCategory' in message)

    def test_create_category_if_parameter_name_is_missing_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/categories', json={})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)

    def test_create_category_if_category_already_exists_then_throws_422(self):
        self.add_data_to_database([5, 2, 1])

        res = self.client().post('/categories', json={
            'name': 'Category1'})
        data = json.loads(res.data)
        self.check_if_operation_failed_with_error_code(data, 422)
