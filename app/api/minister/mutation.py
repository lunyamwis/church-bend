import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.validate_object_id import validate_object_id
from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import Minister
from ..evangelism.models import Evangelism
from app.api.evangelism.models import Evangelism
from .validators.validate_input import MinisterValidations
from .object_types import (
    MinisterInput,MinisterType
)
from datetime import datetime


class CreateMinister(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    minister = graphene.Field(MinisterType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = MinisterInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a minister")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = MinisterValidations()
        data = validator.validate_minister_data(
            kwargs.get("input", ''))
        fields = data.pop("fields", [])
        new_minister = Minister(**data)
        new_minister.save()
        for field in fields:
            field_ = Evangelism.objects.get(id=field)
            new_minister.fields.add(field_)
        return CreateMinister(status="Success", minister=new_minister,
                                    message=SUCCESS_ACTION.format("Minister created"))


class UpdateMinister(graphene.Mutation):
    """
    handles updating of books
    """

    minister = graphene.Field(MinisterType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = MinisterInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update an evangelism field')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        minister_update = validate_object_id(id,Minister,"Minister")
        data = kwargs['input']
        fields = data.pop('fields',[])
        
        for field in fields:
            # import pdb; pdb.set_trace()
            field_ = Evangelism(**field)
            field_.save()
            minister_update.fields.add(field_)

        for (key,value) in data.items():
            setattr(minister_update,key,value)
        minister_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Minister has been updated")

        return UpdateMinister(status = status,minister=minister_update,message=message)




class Mutation(graphene.ObjectType):
    create_minister = CreateMinister.Field()
    update_minister = UpdateMinister.Field()