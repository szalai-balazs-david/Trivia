import json

from app.test.base_test_class import BaseTestClass


class GetCategoryTestCase(BaseTestClass):
    def test_get_categories_returns_list_of_categories(self):
        self.add_data_to_database([1, 2, 1])

        res = self.client().get('/categories')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        self.assertTrue('Category1' in message)
        self.assertTrue('Category2' in message)
        self.assertTrue('Category3' in message)
