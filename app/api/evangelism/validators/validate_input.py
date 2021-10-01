# Third party imports
from app.api.crm.models import ContactManager
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
from ..models import IndividualClient, CorporateClient


class ClientValidations:
    '''Validations for theclient information'''

    def validate_individual_client_registration_data(self, kwargs):
        '''
        Runs all the individual client registration data validations in one function
        Args:
            kwargs (dict): request data
        Returns:
            input_data (dict): validated data
        '''
        check_missing_fields(kwargs, INDIVIDUAL_CLIENT_REQUIRED_FIELD)

        input_data = {}
        input_data['surname'] = kwargs.get('surname', None)
        input_data['first_name'] = kwargs.get('first_name', None)
        input_data['last_name'] = kwargs.get('last_name', None)
        input_data['kra_pin'] = kwargs.get('kra_pin', None)
        input_data['id_number'] = kwargs.get('id_number', None)
        input_data['gender'] = kwargs.get('gender', None)
        input_data['date_of_birth'] = kwargs.get('date_of_birth', None)
        check_empty_fields(data=input_data)
        input_data['email'] = kwargs.get('email', "")
        input_data['town'] = kwargs.get('town', None)
        input_data['contact_persons'] = kwargs.get('contact_persons', [])
        input_data['phone_number'] = kwargs.get('phone_number', "")
        input_data['occupation'] = kwargs.get('occupation', None)
        input_data['postal_address'] = kwargs.get('postal_address', None)
        input_data['agency'] = kwargs.get('agency')
        input_data['status'] = kwargs.get('status', '')
        check_email_validity(
            input_data['email']) if input_data['email'] else ""
        self.validate_gender(input_data['gender'])
        self.validate_item_regex(input_data['kra_pin'], "(\d+[A-Z])|([A-Z]+\d)[\dA-Z]*",
                                 error_dict['invalid_input'].format("KRA PIN"))
        self.validate_item_regex(str(input_data['id_number']), "^([\s\d]+)$",
                                 error_dict['invalid_input'].format("ID number"))
        self.validate_names_length([input_data['first_name'], input_data['last_name']])
        input_data['email'] = self.validate_email_already_exist(
            input_data['email'],
            input_data['agency']) if input_data['email'] else ""
        input_data['phone_number'] = self.validate_phone_number(
            input_data['phone_number'],
            input_data['agency']) if input_data['phone_number'] else ""
        self.validate_id_number_already_exist(
            input_data['id_number'], input_data['agency'])
        self.validate_kra_pin_already_exist(input_data['kra_pin'], input_data['agency'])

        if input_data['contact_persons'] is None:
            input_data['contact_persons'] = []
        _ = [validate_object_id(
            user, ContactManager,
            "Contact Person", input_data['agency']) for user in
            input_data['contact_persons']
            if input_data['contact_persons']]
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

    @ classmethod
    def validate_update_email_already_exist(cls, email, id, agency, model):
        '''
        Checks if email already exists in the db
         Args:
            email (str): user email
            id (str): user id
            agency (obj): agency object
        Raise:
            raise GraphQLError if email already exist
        '''
        if email:
            check_email_validity(email)

            email_existing = model.objects.all_with_deleted().filter(
                email=email, agency=agency).first()

            if email_existing and email_existing.id != id:
                raise GraphQLError(error_dict['already_exist'].format('Client email'))
        return email

    @ classmethod
    def validate_id_number_already_exist(cls, id_number, agency):
        '''
        Checks if id number already exists in the db
         Args:
            id number (str): user id number
            id (str): user id
            agency (obj): agency object
        Raise:
            raise GraphQLError if id number already exist
        '''
        if id_number:
            client = IndividualClient.objects.all_with_deleted().filter(
                id_number=id_number, agency=agency).first()
            if client:
                raise GraphQLError(
                    error_dict['already_exist'].format('Id number'))

    def validate_kra_pin_already_exist(cls, kra_pin, agency):
        '''
        Checks if id number already exists in the db
         Args:
            id number (str): user id number
            id (str): user id
            agency (obj): agency object
        Raise:
            raise GraphQLError if id number already exist
        '''
        if kra_pin:
            client = IndividualClient.objects.all_with_deleted().filter(
                kra_pin=kra_pin, agency=agency).first()
            if client:
                raise GraphQLError(
                    error_dict['already_exist'].format('KRA PIN'))

    @ classmethod
    def validate_update_phone_number_already_exist(cls, phone_number, id, agency, model):
        '''
        Checks if phone number already exists in the db
         Args:
            phone number (str): user phone number
            id (str): user id
            agency (obj): agency object
        Raise:
            raise GraphQLError if phone number already exist
        '''
        if phone_number:
            if not re.match(r'^(?:\B\+ ?254|\b0)', phone_number):
                raise GraphQLError(error_dict['invalid_phone_no'])
            if not re.match(r"(\+254)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})", phone_number):
                raise GraphQLError(
                    error_dict['invalid_input'].format("phone number"))
            client = model.objects.all_with_deleted().filter(
                phone_number=phone_number, agency=agency).first()
            if client and client.id != id:
                raise GraphQLError(
                    error_dict['already_exist'].format('Phone number'))

    @ classmethod
    def validate_email_already_exist(cls, email, agency, model=IndividualClient):
        '''
        Checks if email already exists in the db
         Args:
            email (str): user email
            agency (obj): admin agency
        Raise:
            raise GraphQLError if email already exist
        '''
        try:
            email_existing = model.objects.all_with_deleted().get(
                email=email, agency=agency)
        except ObjectDoesNotExist:
            email_existing = None

        if email_existing and email_existing.is_active:
            raise GraphQLError(error_dict['already_exist'].format('Client email'))
        if email_existing and not email_existing.is_active:
            raise GraphQLError(error_dict['email_already_exist'])
        return email

    @ classmethod
    def validate_phone_number(cls, phone_number, agency, model=IndividualClient):
        '''
        Validates a given phone_number
        Args:
            password (str): phone_number
            agency (obj): admin agency
        Raise:
            raise GraphQLError if phone number is ivalid or exists
        alright
        '''
        if not re.match(r'^(?:\B\+ ?254|\b0)', phone_number):
            raise GraphQLError(error_dict['invalid_phone_no'])
        if not re.match(r"(\+254)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})", phone_number):
            raise GraphQLError(
                error_dict['invalid_input'].format("phone number"))
        if model.objects.all_with_deleted().filter(phone_number=phone_number,
                                                   agency=agency).exists():
            raise GraphQLError(
                error_dict['already_exist'].format('Phone number'))
        return phone_number
