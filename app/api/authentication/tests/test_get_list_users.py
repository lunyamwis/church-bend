from .base import BaseTest
from .mocks import (admin_login_mutation, get_single_user_query,
                    list_users_query)


class TestGetListUsers(BaseTest):
    """
    List users tests
    """

    def test_get_user_succeeds(self):
        """
        Test get user details using user ID
        """
        self.create_and_activate_admin()
        res = self.client.execute(admin_login_mutation)
        response = self.client.execute(
            get_single_user_query,
            {"id": res.data['tokenAuth']['user']['id']})
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertEqual(data['user']['username'], "Admin")
        self.assertEqual(data['user']['email'], "test-email@gmail.com")

    def test_list_users_succeeds(self):
        """
        Test get users details
        """
        self.create_and_activate_admin()
        self.client.execute(admin_login_mutation)
        response = self.client.execute(list_users_query)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertEqual(data['users']['items'][0]['username'], "Admin")
        self.assertEqual(data['users']['items'][0]['email'], "test-email@gmail.com")
        self.assertEqual(data['users']['page'], 1)
