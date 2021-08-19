from functools import wraps

from django.contrib.auth.models import AnonymousUser
from graphql import GraphQLError
from rolepermissions.checkers import has_permission, has_role

from .jwt_errors import error_dict


def permission_required(user, permissions, message):
    """
    Permission required decorator determines if a given user has permission
    Args:
        user (obj): user to check permission
        permissions (list): a list of permissions
        message (string): error message to return if permission is denied
    Raises:
        ValidationError: is raised if user has no permissions on a resource
    """
    is_permitted = False
    for permission in permissions:
        if has_permission(user, permission) and user.is_active:
            is_permitted = True
    if not is_permitted:
        raise GraphQLError(message)


def role_required(user, roles, message):
    """
    Role required decorator determines if a given user has role
    Args:
        roles(list): a list of role
        user (obj): user to check role
        message (string): error message to return if user has no such role

    Raises:
        ValidationError: is raised if user has no permissions on a resource
    """
    is_permitted = False
    for role in roles:
        if has_role(user, role) and user.is_active:
            is_permitted = True
    if not is_permitted:
        raise GraphQLError(message)


def token_required(func):
    """Authentication decorator. Validates token from the client

    Args:
        func (function): Function to be decorated

    Returns:
        function: Decorated function

    Raises:
        ValidationError: Validation error
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        _, info = args
        user = info.context.user
        bearer_token = info.context.headers.get('Authorization', '')
        if bearer_token and bearer_token.split(" ")[0] != 'JWT':
            raise GraphQLError(error_dict['NO_BEARER_MSG'])
        if isinstance(user, AnonymousUser):

            raise GraphQLError(error_dict['NO_TOKEN_MSG'])
        return func(*args, **kwargs)

    return decorated_function
