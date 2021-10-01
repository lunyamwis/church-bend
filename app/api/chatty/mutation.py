import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.validate_object_id import validate_object_id
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Chat,Group,Thread
)
from .validators.validate_input import ChatValidations
from .object_types import (
    GroupInput,GroupType,
    ChatInput,ChatType
)
from datetime import datetime


class CreateChat(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    chat = graphene.Field(ChatType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = ChatInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a chat")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = ChatValidations()
        data = validator.validate_chat_data(
            kwargs.get("input", ''))
        groups = data.pop("group", [])
        new_chat = Chat(**data)
        new_chat.save()
        for group in groups:
            group_ = Group.objects.get(id=group)
            new_chat.group.add(group_)
        return CreateChat(status="Success", chat=new_chat,
                                    message=SUCCESS_ACTION.format("Chat created"))

class UpdateChat(graphene.Mutation):
    """
    handles updating of books
    """

    chat = graphene.Field(ChatType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = ChatInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a chat')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        chat_update = validate_object_id(id,Chat,"Chat")
        data = kwargs['input']
        if data.get('thread',None):
            data['thread'] = validate_object_id(
                data['thread'], Thread,
                "thread")

        groups = data.pop('group',[])
        for group in groups:
            add_group = Group(**group)
            add_group.save()
            chat_update.group.add(add_group)

        for (key,value) in data.items():
            setattr(chat_update,key,value)
        chat_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Chats have been updated")

        return UpdateChat(status = status,chat=chat_update,message=message)

class Mutation(graphene.ObjectType):
    create_chat = CreateChat.Field()
    update_chat = UpdateChat.Field()