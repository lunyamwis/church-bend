import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.validate_object_id import validate_object_id
from ..helpers.constants import SUCCESS_ACTION
from ..minister.models import Minister
from ..ministry.models import Ministry
from .models import Donations
from .validators.validate_input import DonationValidations
from .object_types import (
    DonationType,DonationInput
)
from datetime import datetime


class CreateDonation(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    donation = graphene.Field(DonationType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = DonationInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a donation")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = DonationValidations()
        data = validator.validate_donation_data(
            kwargs.get("input", ''))
        new_donation = Donations(**data)
        new_donation.save()
        return CreateDonation(status="Success", donation=new_donation,
                                      message=SUCCESS_ACTION.format("Donation added"))

class UpdateDonation(graphene.Mutation):
    """
    handles updating of books
    """

    donation = graphene.Field(DonationType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = DonationInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a donation')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        donation_update = validate_object_id(id,Donations,"Donations")
        data = kwargs['input']
        if data.get('minister',None):
            data['minister'] = validate_object_id(
                data['minister'], Minister,
                "minister")

        if data.get('ministry',None):
            data['ministry'] = validate_object_id(
                data['ministry'], Ministry,
                "ministry")

        
        for (key,value) in data.items():
            setattr(donation_update,key,value)
        donation_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Donations have been updated")

        return UpdateDonation(status = status,donation=donation_update,message=message)

class Mutation(graphene.ObjectType):
    create_donation = CreateDonation.Field()
    update_donation = UpdateDonation.Field()