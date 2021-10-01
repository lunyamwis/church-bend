import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from app.api.evangelism.object_types import (EvangelismInput,EvangelismType)
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import Minister


class MinisterType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Minister

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()





class MinisterInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    first_name = graphene.String()
    last_name = graphene.String()
    other_names = graphene.String()
    email = graphene.String()
    contact_assistant_name = graphene.String()
    contact_assistant_email = graphene.String()
    conference_name = graphene.String()
    fields = graphene.List(EvangelismInput)
    home_church_name = graphene.String()
    home_church_email = graphene.String()
    home_church_phone_numbers = graphene.String()
    home_church_location = graphene.String()
    church_elder_first_name = graphene.String()
    church_elder_last_name = graphene.String()

    


class MinisterPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(MinisterType)
