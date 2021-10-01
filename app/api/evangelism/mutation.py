import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.validate_object_id import validate_object_id
from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..minister.models import Minister
from ..member.models import Member
from ..ministry.models import Ministry
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Evangelism
)
from .object_types import (EvangelismType,EvangelismInput)
from datetime import datetime


class CreateEvangelism(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    field = graphene.Field(EvangelismType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = EvangelismInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a field")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        data = kwargs['input']
        new_field = Evangelism(**data)
        new_field.save()
        return CreateEvangelism(status="Success", field=new_field,
                                      message=SUCCESS_ACTION.format("Field created"))


class UpdateEvangelism(graphene.Mutation):
    """
    handles updating of books
    """

    field = graphene.Field(EvangelismType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = EvangelismInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update an evangelism field')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        field_update = validate_object_id(id,Evangelism,"Evangelism")
        data = kwargs['input']

        if data.get('member',None):
            data['member'] = validate_object_id(
                data['member'], Member,
                "member")

        if data.get('minister',None):
            data['minister'] = validate_object_id(
                data['minister'], Minister,
                "minister")

        if data.get('ministry',None):
            data['ministry'] = validate_object_id(
                data['ministry'], Ministry,
                "ministry")

        
        for (key,value) in data.items():
            setattr(field_update,key,value)
        field_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Evangelism Field has been updated")

        return UpdateEvangelism(status = status,field=field_update,message=message)



class Mutation(graphene.ObjectType):
    create_field = CreateEvangelism.Field()
    update_field = UpdateEvangelism.Field()
