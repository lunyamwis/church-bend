from .base import BaseTest
from .mocks import user_signup_mutation


class TestSignup(BaseTest):
    """
    Signup tests
    """

    def test_admin_signup_succeeds(self):
        """
        Test admin signup with valid data succeeds
        """
        response = self.create_admin_user()
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.activate_account(data['createAdmin']['admin']['email'],
        data['createAdmin']['admin']['agency']['agencyEmail'],
        data['createAdmin']['admin']['agency']['id'])
        self.assertEqual(data['createAdmin']['status'], "Success")
        self.assertEqual(data['createAdmin']['admin']['email'], "test-email@gmail.com")
        self.assertEqual(data['createAdmin']['admin']['roles'][0], "admin")
        self.assertEqual(data['createAdmin']['admin']['agency']['name'], 'Samar Insurance')

    def test_user_signup_succeeds(self):
        """
        Test user signup with valid data succeeds
        """
        self.create_and_activate_admin()
        response = self.create_user()
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertEqual(data['createUser']['status'], "Success")
        self.assertEqual(data['createUser']['user']['email'], "jane@example.com")
        self.assertEqual(data['createUser']['user']['roles'][0], "manager")
        self.assertEqual(data['createUser']['user']['agency']['name'], 'Samar Insurance')

    def test_user_activation_succeeds(self):
        """
        Test user signup with valid data succeeds
        """
        response = self.create_admin_user()
        data = dict(response.data)
        res = self.activate_account(data['createAdmin']['admin']['email'],
        data['createAdmin']['admin']['agency']['agencyEmail'],
        data['createAdmin']['admin']['agency']['id'])
