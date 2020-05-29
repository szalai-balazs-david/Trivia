import json

from app.test.base_test_class import BaseTestClass


class GetUserTestCase(BaseTestClass):
    def test_get_users_returns_list_of_users(self):
        self.add_user_to_database([
            {'name': 'User1', 'wins': 2, 'answers': 5},
            {'name': 'User2', 'wins': 2, 'answers': 5}])

        res = self.client().get('/users')
        data = json.loads(res.data)
        message = self.check_if_operation_was_successful_and_get_payload(data)

        found1 = False
        found2 = False
        for user in message:
            if user['name'] == 'User1':
                found1 = True
            if user['name'] == 'User2':
                found2 = True
        self.assertTrue(found1)
        self.assertTrue(found2)
