from graphql import GraphQLError

from ...helpers.validation_errors import error_dict
from ..models import User
import app.api.roles.roles


def validate_user_email(email):
    '''
    Checks if user with that email exists in the db
    Args:
        email (str): user email
    Raise:
        raise GraphQLError if email does not exist
    Return:
        user (obj): user object
    '''
    user = User.objects.filter(email=email).first()
    if not user:
        raise GraphQLError(error_dict['does_not_exist'].format('User'))
    return user


def get_roles():
    '''
    Get available roles
    Return:
        available_roles (list): get available roles
    '''
    available_roles = []
    try:
        for attribute_name in dir(app.api.roles.roles):
            attribute = getattr(app.api.roles.roles, attribute_name)
            if issubclass(
                attribute,
                app.api.roles.roles.AbstractUserRole) \
                    and attribute_name != 'AbstractUserRole':
                available_roles.append(attribute_name)
    except TypeError:
        pass
    return available_roles


def create_username_slug(username):
    """This method automatically slugs the username before saving"""
    slug = username
    new_slug = slug
    n = 1
    while User.objects.all_with_deleted().filter(username=new_slug).exists():
        new_slug = '{}-{}'.format(slug, n)
        n += 1

    return new_slug
