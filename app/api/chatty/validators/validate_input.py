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
from ..models import (
    Chat,Group,Thread
)


class ChatValidations:
    '''Validations for theclient information'''

    def validate_chat_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        input_data['delivered'] = kwargs.get('delivered',None)
        input_data['read'] = kwargs.get('read',None)
        input_data['text'] = kwargs.get('text',None)
        input_data['response'] = kwargs.get('response',None)
        input_data['email'] = kwargs.get('email',None)
        input_data['sms'] = kwargs.get('sms',None)
        input_data['chat_type'] = kwargs.get('chat_type',None)
        input_data['sender'] = kwargs.get('sender',None)
        input_data['receiver'] = kwargs.get('receiver',None)
        input_data['thread'] = kwargs.get('thread',None)
        input_data['group'] = kwargs.get('group',[])

        return input_data

