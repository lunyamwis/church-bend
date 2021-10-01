import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import (
    Chat,Group,Thread
)

class ThreadType(DjangoObjectType):
    class Meta:
        model = Thread

class ThreadInput(graphene.InputObjectType):
    name = graphene.String()

class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class GroupInput(graphene.InputObjectType):
    name = graphene.String()

class ChatType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Chat

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()


class ChatInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    delivered=graphene.Boolean()
    read = graphene.Boolean()
    text = graphene.String()
    response = graphene.String()
    email = graphene.String()
    sms = graphene.String()
    chat_type = graphene.String()
    sender = graphene.String()
    receiver = graphene.String()
    thread = graphene.String()
    group  = graphene.List(GroupInput)

    
class ChatPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(ChatType)
