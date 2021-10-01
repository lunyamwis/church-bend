# Third party imports
import re

# Local imports
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

from ...helpers.constants import (BLOG_REQUIRED_FIELD,
                                  GENDER_OPTIONS, CORPORATE_CLIENT_REQUIRED_FIELD)
from ...helpers.validate_input import (check_email_validity,
                                       check_empty_fields,
                                       check_missing_fields)
from ...helpers.validation_errors import error_dict
from ...helpers.validate_object_id import validate_object_id
from ..models import Blog, Comments, Tags, Category
from ...authentication.models import User


class BlogValidations:
    '''Validations for theclient information'''

    def validate_blog_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''
        check_missing_fields(kwargs, BLOG_REQUIRED_FIELD)

        input_data = {}
        input_data['title'] = kwargs.get('title', None)
        input_data['post'] = kwargs.get('post', None)
        input_data['summary'] = kwargs.get('summary', None)
        check_empty_fields(data=input_data)
        input_data['status'] = kwargs.get('status', None)
        input_data['published'] = kwargs.get('published', None)
        input_data['category'] = kwargs.get('category', [])
        input_data['tags'] = kwargs.get('tags', [])
        input_data['comments'] = kwargs.get('comments', None)
        input_data['author'] = kwargs.get('author', None)

        if input_data['tags'] is None:
            input_data['tags'] = []

        if input_data['category'] is None:
            input_data['category'] = []

        if input_data['comments']:
            input_data['comments'] = validate_object_id(
                input_data['comments'], Comments,
                "Comments")

        if input_data['author']:
            input_data['author'] = validate_object_id(
                input_data['author'], User,
                "User")

        return input_data

    def validate_comment_data(self, kwargs):

        input_data = {}
        input_data['title'] = kwargs.get('title', None)
        input_data['content'] = kwargs.get('content', None)
        input_data['creator'] = kwargs.get('creator', None)
        input_data['status'] = kwargs.get('status', None)
        input_data['blog'] = kwargs.get('blog', None)

        if input_data['creator']:
            input_data['creator'] = validate_object_id(
                input_data['creator'], User, "User"
            )

        if input_data['blog']:
            input_data['blog'] = validate_object_id(
                input_data['blog'], Blog, "Blog"
            )
        return input_data

    def validate_category_data(self, kwargs):

        input_data = {}
        input_data['title'] = kwargs.get('title', None)
        input_data['content'] = kwargs.get('content', None)
        
        return input_data

    def validate_tags_data(self,kwargs):
        input_data = {}
        input_data['title'] = kwargs.get('title', None)
        input_data['content'] = kwargs.get('content', None)
        
        return input_data


    def validate_corporate_client_registration_data(self, kwargs):
        '''
        Runs all the corporate client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''
        check_missing_fields(kwargs, CORPORATE_CLIENT_REQUIRED_FIELD)

        input_data = {}
        input_data['name'] = kwargs.get('name', None)
        check_empty_fields(data=input_data)
        input_data['email'] = kwargs.get('email', None)
        input_data['phone_number'] = kwargs.get('phone_number', None)
        input_data['kra_pin'] = kwargs.get('kra_pin', None)
        input_data['contact_persons'] = kwargs.get('contact_persons', [])
        input_data['town'] = kwargs.get('town', None)
        input_data['about'] = kwargs.get('about', None)
        input_data['postal_address'] = kwargs.get('postal_address', None)
        input_data['agency'] = kwargs.get('agency')
        input_data['status'] = kwargs.get('status')
        input_data['facebook_account'] = kwargs.get('facebook_account')
        input_data['twitter_account'] = kwargs.get('twitter_account')
        input_data['instagram_account'] = kwargs.get('instagram_account')
        input_data['linkedin_account'] = kwargs.get('linkedin_account')
        check_email_validity(input_data['email']) if input_data['email'] else ""
        input_data['phone_number'] = self.validate_phone_number(
            input_data['phone_number'],
            input_data['agency'], CorporateClient) if input_data['phone_number'] else ""
        input_data['email'] = self.validate_email_already_exist(
            input_data['email'], input_data['agency'],
            CorporateClient) if input_data['email'] else ""
        self.validate_kra_pin_already_exist(input_data['kra_pin'], input_data['agency'])

        if input_data['contact_persons'] is None:
            input_data['contact_persons'] = []
        _ = [validate_object_id(
            user, ContactManager,
            "Contact Person", input_data['agency']) for user in
            input_data['contact_persons']
            if input_data['contact_persons']]
        return input_data

    def validate_corporate_client_update_data(self, data, client_id, user):
        '''
        Runs all  user update data validations in one function
        Args:
            data (dict): request data
            client_id (str): client id
            user (obj): manager
        Returns:
            input_data (dict): validated data
        '''
        validate_object_id(client_id, CorporateClient, "Corporate Client", user.agency)

        data_ = check_empty_fields(data)

        self.validate_update_email_already_exist(data_.get('email', ''), client_id,
                                                 user.agency, CorporateClient)
        self.validate_update_phone_number_already_exist(data_.get('phone_number', ''),
                                                        client_id, user.agency,
                                                        CorporateClient)

        if data_.get('kra_pin', ''):
            self.validate_item_regex(
                data_.get('kra_pin', ''), "(\d+[A-Z])|([A-Z]+\d)[\dA-Z]*",
                error_dict['invalid_input'].format("KRA PIN"))
        elif data_.get('id_number', ''):
            self.validate_item_regex(str(data_.get('id_number', '')), "^([\s\d]+)$",
                                     error_dict['invalid_input'].format("ID number"))
        if data_.get('contact_persons') is None:
            data_['contact_persons'] = []
        _ = [validate_object_id(
            u, ContactManager,
            "Contact Person", user.agency) for u in
            data_['contact_persons']
            if data_['contact_persons']]
        return data_

    def validate_individual_client_update_data(self, data, client_id, user):
        '''
        Runs all  user update data validations in one function
        Args:
            data (dict): request data
            client_id (str): client id
            user (obj): manager
        Returns:
            input_data (dict): validated data
        '''
        validate_object_id(client_id, IndividualClient, "Individual Client", user.agency)
        data_ = check_empty_fields(data)

        self.validate_update_email_already_exist(data_.get('email', ''), client_id,
                                                 user.agency, IndividualClient)
        self.validate_update_phone_number_already_exist(data_.get('phone_number', ''),
                                                        client_id, user.agency,
                                                        IndividualClient)

        if data_.get('gender', ''):
            self.validate_gender(data_.get('gender', ''))
        elif data_.get('kra_pin', ''):
            self.validate_item_regex(
                data_.get('kra_pin', ''), "(\d+[A-Z])|([A-Z]+\d)[\dA-Z]*",
                error_dict['invalid_input'].format("KRA PIN"))
        elif data_.get('id_number', ''):
            self.validate_item_regex(str(data_.get('id_number', '')), "^([\s\d]+)$",
                                     error_dict['invalid_input'].format("ID number"))

        if data_.get('contact_persons') is None:
            data_['contact_persons'] = []
        _ = [validate_object_id(
            u, ContactManager,
            "Contact Person", user.agency) for u in
            data_['contact_persons']
            if data_['contact_persons']]
        return data_

    def validate_names_length(self, names):
        '''
        Checks if the names has at least 3 characters
        Args:
            names (list): user names
        Raise:
            raise GraphQLError if name is too short
        '''
        for name in names:
            if len(name) <= 2:
                raise GraphQLError(error_dict['min_length'].format('Name', 3))

    def validate_gender(self, gender):
        '''
        Checks if the gender value is valid
        Args:
            gender (str): vender value
        Raise:
            raise GraphQLError if gender is invalid
        '''
        if gender.upper() not in [*GENDER_OPTIONS]:
            raise GraphQLError(
                error_dict['valid_options'].format('gender', [*GENDER_OPTIONS]))

    def validate_item_regex(self, item, regex, message):
        '''
        Checks if the item is valid based on the regex
        Args:
            item (str): item to validate
            regex (str): regex to validate
            message (str): validation error message
        Raise:
            raise GraphQLError if items invalid
        '''
        if not re.match(r'{}'.format(regex), item):
            raise GraphQLError(message)
