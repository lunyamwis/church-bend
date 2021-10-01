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
from ..models import Donations
from app.api.minister.models import Minister
from app.api.ministry.models import Ministry

class DonationValidations:
    '''Validations for theclient information'''

    def validate_donation_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        input_data['first_name'] = kwargs.get('first_name',None)
        input_data['last_name'] = kwargs.get('last_name',None)
        input_data['donation_type'] = kwargs.get('donation_type',None)
        input_data['amount'] = kwargs.get('amount',None)
        input_data['notes'] = kwargs.get('notes',None)
        input_data['ministry'] = kwargs.get('ministry',None)
        input_data['minister'] = kwargs.get('minister',None)
        input_data['monthly'] = kwargs.get('monthly',None)

        if input_data['ministry']:
            input_data['ministry'] = validate_object_id(
                input_data['ministry'], Ministry, "Ministry"
            )

        if input_data['minister']:
            input_data['minister'] = validate_object_id(
                input_data['minister'], Minister, "Minister"
            )
        return input_data

    