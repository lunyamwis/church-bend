from .base import BaseTest
from .mocks import update_user_mutation, admin_login_mutation


class TestUpdateUser(BaseTest):
    """
    Update user tests
    """

    def test_update_user_succeeds(self):
        """
        Test update user with valid data succeeds
        """
        self.create_and_activate_admin()
        self.client.execute(admin_login_mutation)
        response = self.client.execute(update_user_mutation)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertEqual(data['updateUser']['status'], "Success")
        self.assertEqual(data['updateUser']['user']['firstName'], "Test")
