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
from ..models import (Video,Tags,Categories)


class VideoValidations:
    '''Validations for theclient information'''

    def validate_video_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        input_data['title'] = kwargs.get('title',None)
        input_data['description'] = kwargs.get('description',None)
        input_data['tags'] = kwargs.get('tags',[])
        input_data['categories'] = kwargs.get('categories',[])
        input_data['video'] = kwargs.get('video',None)
        return input_data

    def validate_premium_videos_data(self, kwargs):
        '''
        Runs all the corporate client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        input_data['name'] = kwargs.get('name', None)
        input_data['price'] = kwargs.get('price',None)
        input_data['paid'] = kwargs.get('paid',None)
        input_data['content'] = kwargs.get('content',[])

        return input_data
