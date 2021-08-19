from .base import BaseTest
from .mocks import (admin_login_mutation, roles_query, permission_query)


class TestGetRolesAndPermissions(BaseTest):
    """
    Get roles and permissions
    """


    def test_list_roles_succeeds(self):
        """
        Test get roles
        """
        self.create_and_activate_admin()
        self.client.execute(admin_login_mutation)
        response = self.client.execute(roles_query)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertIn("Admin", data['roles'])

    def test_get_role_permission_succeeds(self):
        """
        Test get permissions
        """
        self.create_and_activate_admin()
        self.client.execute(admin_login_mutation)
        response = self.client.execute(permission_query)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, dict)
        data = dict(response.data)
        self.assertIn("create_client_record", data['rolePermissions'])
