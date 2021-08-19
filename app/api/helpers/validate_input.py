# Third party imports
import re
from graphql import GraphQLError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Local imports
from .validation_errors import error_dict


def check_empty_fields(data):
    '''
    Checks if empty fields are submitted
    Args:
        data (dict): request data
    Raise:
        raise GraphQLError if field is empty'''
    valid = {}
    for field in data:
        if not data[field]:
            raise GraphQLError(
                error_dict['empty_field'].format(" ".join(field.title().split("_"))))
        valid.update({field: data[field]})
    return valid


def check_email_validity(email):
    '''
    Check if the given mail is valid
    Args:
        email (str): user email
    Raise:
        raise GraphQLError if email is invalid'''
    try:
        validate_email(email)
    except ValidationError:
        raise GraphQLError(error_dict['invalid_input'].format('email'))


def check_missing_fields(data, required_fields):
    '''
    Checks for missing field
    Args:
        data (dict): request data
        required_fields (list): required fields
    Raise:
        raise GraphQLError if field is missing
    '''
    missing_fields = []
    if isinstance(data, list):
        for i in data:
            missing_fields = [item for item in required_fields if item not in [*i]]
    else:
        missing_fields = [item for item in required_fields if item not in [*data]]
    if missing_fields:
        raise GraphQLError(error_dict['required'].format(missing_fields))


def validate_phone_number(phone_number, model):
    '''
    Validates a given phone_number
    Args:
        password (str): phone_number
        model (obj): model to validate
    Raise:
        raise GraphQLError if phone number is ivalid or exists
    '''
    if not re.match(r'^(?:\B\+ ?254|\b0)', phone_number):
        raise GraphQLError(error_dict['invalid_phone_no'])
    if not re.match(r"(\+254)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})", phone_number):
        raise GraphQLError(
            error_dict['invalid_input'].format("phone number"))
    if model.objects.all_with_deleted().filter(phone_number=phone_number).exists():
        raise GraphQLError(
            error_dict['already_exist'].format('Phone number'))


def validate_image_url(image_url):
    '''
    Validates a given image_url
    Args:
        image_url (str): image url
    Raise:
        raise GraphQLError if image url is ivalid
    '''
    if image_url and not re.match(r'^(http(s?):)|([/|.|\w|\s])*\.(?:jpg|gif|png)',
                                  image_url):
        raise GraphQLError(error_dict['invalid_input'].format("image url"))
