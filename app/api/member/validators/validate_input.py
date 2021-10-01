# Third party imports
import re

# Local imports
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

from ...helpers.constants import (INDIVIDUAL_CLIENT_REQUIRED_FIELD,
                                  GENDER_OPTIONS, CORPORATE_CLIENT_REQUIRED_FIELD)
from ...helpers.validate_input import (check_email_validity,
                                       check_empty_fields,
                                       check_missing_fields)
from ...helpers.validation_errors import error_dict
from ...helpers.validate_object_id import validate_object_id
from ..models import (Member)


class MemberValidations:
    '''Validations for theclient information'''

    def validate_member_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        check_empty_fields(data=input_data)
        input_data['conference_name'] = kwargs.get('conference_name',None)
        input_data['field_name'] = kwargs.get('field_name',None)
        input_data['home_church_name'] = kwargs.get('home_church_name',None)
        input_data['home_church_email'] = kwargs.get('home_church_email',None)
        input_data['home_church_phone_numbers'] = kwargs.get('home_church_phone_numbers',None)
        input_data['home_church_location'] = kwargs.get('home_church_location',None)
        input_data['church_elder_first_name'] = kwargs.get('church_elder_first_name',None)
        input_data['church_elder_last_name'] = kwargs.get('church_elder_last_name',None)
        input_data['occupation'] = kwargs.get('occupation',None)
        input_data['baptized'] = kwargs.get('baptized',None)
        input_data['position_church'] = kwargs.get('position_church',None)
        return input_data
