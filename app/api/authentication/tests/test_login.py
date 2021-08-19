from .base import BaseTest
from .mocks import admin_login_mutation


class TestLogin(BaseTest):
    """
    Signup tests
    """

    def test_login_succeeds(self):
        """
        Test login with valid data succeeds
        """

        response = self.create_and_activate_admin()
        response = self.client.execute(admin_login_mutation)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)

        data = dict(response.data)
        self.assertEqual(data['tokenAuth']['payload']['username'], "Admin")
        self.assertIsInstance(data['tokenAuth']['token'], str)
