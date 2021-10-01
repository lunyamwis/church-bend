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
    Podcast,Tags,Category
)


class PodcastValidations:
    '''Validations for theclient information'''

    def validate_podcast_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''

        input_data = {}
        input_data['name'] = kwargs.get('name',None)
        input_data['sort_by_date'] = kwargs.get('sort_by_date',None)
        input_data['podcast_type'] = kwargs.get('podcast_type',None)
        input_data['duration'] = kwargs.get('duration',None)
        input_data['published'] = kwargs.get('published',None)
        input_data['language'] = kwargs.get('language',None)
        input_data['region'] = kwargs.get('region',None)
        input_data['podcast'] = kwargs.get('podcast',None)
        input_data['tags'] = kwargs.get('tags',[])
        input_data['categories'] = kwargs.get('categories',[])
        
        return input_data

    def validate_premium_podcast_data(self, kwargs):
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

