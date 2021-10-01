# Third party imports
import re

from app.api.roles.roles import Admin, Manager
from django.contrib.auth.password_validation import validate_password
# Local imports
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from graphql import GraphQLError

from ...helpers.constants import USER_REQUIRED_FIELD
from ...helpers.validate_input import (check_email_validity,
                                       check_empty_fields,
                                       check_missing_fields,
                                       validate_image_url)
from ...helpers.validation_errors import error_dict
from ..helpers.user_helpers import get_roles
from ..models import User


class UserValidations:
    '''Validations for the user email, username and password'''

    def validate_user_registration_data(self, kwargs):
        '''
        Runs all the user registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''
        check_missing_fields(kwargs, USER_REQUIRED_FIELD)

        input_data = {}
        input_data['username'] = kwargs.get('username', None)
        input_data['email'] = kwargs.get('email', None)
        input_data['password'] = kwargs.get('password', None)
        input_data['first_name'] = kwargs.get('first_name', None)
        input_data['phone_number'] = kwargs.get('phone_number', None)
        check_empty_fields(data=input_data)
        input_data['image'] = kwargs.get('image', None)
        input_data['member'] = kwargs.get('member',None)
        input_data['ministry'] = kwargs.get('ministry',None)
        input_data['minister'] = kwargs.get('minister',None)
        check_email_validity(input_data['email'])
        self.validate_password(input_data['password'])
        self.validate_username(input_data['username'])
        validate_image_url(input_data['image'])
        return input_data

    def validate_user_update_data(self, data, user):
        '''
        Runs all  user update data validations in one function
        Args:
            data (dict): request data
        Returns:
            input_data (dict): validated data
        '''
        validators = {
            "username": self.validate_username,
            "image": validate_image_url,
            "first_name": self.validate_name_length,
            "last_name": self.validate_name_length,
            "password": self.validate_password
        }
        # "phone_number": self.validate_phone_number,
        input_data = {}
        check_empty_fields(data)
        for item in data:
            validate = validators.get(item, None)
            if validate:
                validate(data.get(item))
            input_data.update({item: data.get(item)})
        return input_data

    def validate_username(self, username):
        '''
        Checks if the username already exist
        Args:
            username (str): username
        Raise:
            raise GraphQLError if username already exist
        '''
        self.validate_name_length(username)

        if User.objects.all_with_deleted().filter(username=username).exists():
            raise GraphQLError(error_dict['already_exist'].format('Username'))

    def validate_name_length(self, name):
        '''
        Checks if the name has at least 3 characters
        Args:
            name (str): user name
        Raise:
            raise GraphQLError if name is too short
        '''
        if len(name) <= 2:
            raise GraphQLError(error_dict['min_length'].format('Name', 3))

    
    @classmethod
    def check_active_and_verified_status(cls, email):
        '''checks whether the account is deactivated or unverified'''
        try:
            email_existing = User.objects.get(email=email)
        except ObjectDoesNotExist:
            email_existing = None

        if email_existing and email_existing.is_deactivated:
            raise GraphQLError(error_dict['account_deactivated'])
        if email_existing and not email_existing.is_verified:
            raise GraphQLError(error_dict['account_deactivated'])

    @classmethod
    def validate_user_role(cls, role):
        '''
        Validates a given role exists
        Args:
            role (str): role to validate
        Raise:
            raise GraphQLError if role does not exist
        '''
        default_roles = {
            "manager": Manager,
            "admin": Admin
        }
        available_roles = get_roles()
        role_ = [r for r in available_roles if r.lower() == role.lower()]
        if role_:
            model = default_roles.get(role.lower())
            return model.available_permissions

        raise GraphQLError(error_dict['does_not_exist'].format("Role"))

    @classmethod
    def validate_password(cls, password):
        '''
        Validates a given password
        Args:
            passsword (str): password input
        Raise:
            raise GraphQLError if password is invalid'''
        try:
            validate_password(password)
        except ValidationError as error:
            raise GraphQLError(error.messages)

    