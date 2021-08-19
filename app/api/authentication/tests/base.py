
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphene.test import Client
from django.test.testcases import TestCase
from django.db import IntegrityError
from unittest.mock import patch, Mock

from ..models import User
from ..schema import schema
from .mocks import (user_login_mutation, user_one, user_signup_mutation,
                    admin_signup_mutation, admin_login_mutation)
from ...helpers.jwt_helper import generate_jwt

# @pytest.mark.django_db
class BaseTest(JSONWebTokenTestCase, TestCase):
    """
    API base test case
    """
    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/api/v1/graphql/'

    def create_user(self):
        """
        Create test user
        Return:
            User obj (obj): signup response object
        """
        user = User.objects.create_user(**user_one)
        user.is_active=True
        user.save()
        return user

    @patch("app.api.helpers.tasks.send_mail_.delay", Mock(return_value=True))
    def create_admin_user(self):
        """
        Signup user
        Return:
            response (obj): signup response object
        """
        response = self.client.execute(admin_signup_mutation)
        return response

    @patch("app.api.helpers.tasks.send_mail_.delay", Mock(return_value=True))
    def create_user(self):
        """
        Signup user
        Return:
            response (obj): signup response object
        """
        response = self.client.execute(user_signup_mutation)
        return response

    def activate_account(self, user_email, agency_email, agency_id):
        """
        Activate user
        Args:
            agency_email (str): agency email to generate jwt and activate user
            user_email (str): user email to generate jwt and activate user
        """
        client = TestCase.client_class()
        agent_activation_url = self.GRAPHQL_URL+'agencies/activate/{}'.format(generate_jwt(agency_email, agency_id))
        admin_activation_url = self.GRAPHQL_URL+'users/activate/{}'.format(generate_jwt(user_email, agency_id))
        client.get(agent_activation_url)
        return client.get(admin_activation_url)


    def create_and_activate_admin(self):
        """
        Create and activate admin
        Return:
            agency_email (str): agency email to generate jwt and activate user
            user_email (str): user email to generate jwt and activate user
        """
        res = self.create_admin_user()
        data = res.data
        self.activate_account(data['createAdmin']['admin']['email'],
        data['createAdmin']['admin']['agency']['agencyEmail'],
        data['createAdmin']['admin']['agency']['id'])
        response = self.client.execute(admin_login_mutation)
        self.client.credentials(HTTP_AUTHORIZATION="JWT "+response.data['tokenAuth']['token'])
        return response.data['tokenAuth']['token']

    def login_user(self):
        """
        Login user
        Return:
            response (obj): login response object
        """
        try:
            self.create_user()
        except IntegrityError:
            pass
        response = self.client.execute(user_login_mutation)
        return response
    def enable_auth_header(self):
        """
        Add token to auth header and authenticates the client
        Returns
            response.data['tokenAuth'] (str): token
        """
        try:
            self.create_user()
        except IntegrityError:
            pass
        response = self.client.execute(user_login_mutation)
        token = response.data['tokenAuth']['token']
        self.client.credentials(HTTP_AUTHORIZATION="JWT "+token)
        return response.data['tokenAuth']
