import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from app.api.evangelism.models import Evangelism
from .models import Ministry
from .validators.validate_input import MinistryValidation
from .object_types import (
    MinistryInput,MinistryType
)
from datetime import datetime


class CreateMinistry(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    ministry = graphene.Field(MinistryType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = MinistryInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a ministry")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = MinistryValidation()
        data = validator.validate_ministry_data(
            kwargs.get("input", ''))
        fields = data.pop("fields", [])
        new_ministry = Ministry(**data)
        new_ministry.save()
        for field in fields:
            field_ = Evangelism.objects.get(id=field)
            new_ministry.fields.add(field_)
        return CreateMinistry(status="Success", ministry=new_ministry,
                                      message=SUCCESS_ACTION.format("Ministry created"))


class Mutation(graphene.ObjectType):
    create_ministry = CreateMinistry.Field()