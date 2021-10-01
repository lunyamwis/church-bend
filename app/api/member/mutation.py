import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.validate_object_id import validate_object_id
from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Member
)
from .validators.validate_input import MemberValidations
from .object_types import (
    MemberInput,MemberType
)
from datetime import datetime


class CreateMember(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    member = graphene.Field(MemberType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = MemberInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a member")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = MemberValidations()
        data = validator.validate_member_data(
            kwargs.get("input", ''))
        new_member = Member(**data)
        new_member.save()
        return CreateMember(status="Success", member=new_member,
                                      message=SUCCESS_ACTION.format("Member created"))


class UpdateMember(graphene.Mutation):
    """
    handles updating of books
    """

    member = graphene.Field(MemberType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = MemberInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update an evangelism field')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        member_update = validate_object_id(id,Member,"Member")
        data = kwargs['input']

        
        for (key,value) in data.items():
            setattr(member_update,key,value)
        member_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Member has been updated")

        return UpdateMember(status = status,member=member_update,message=message)




class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()
    update_member = UpdateMember.Field()
    
