import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import Evangelism


class EvangelismType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Evangelism

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()


class EvangelismInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    field = graphene.String()
    event = graphene.String()
    event_name = graphene.String()
    event_date = graphene.Date()
    event_location = graphene.String()
    event_purpose = graphene.String()
    event_duration = graphene.String()
    sermon_theme = graphene.String()
    sermon_length = graphene.Float()
    number_attendees = graphene.Float()
    budget = graphene.Float()
    number_converts = graphene.Float()
    number_followups = graphene.Float()
    minister = graphene.String()
    member = graphene.String()
    ministry = graphene.String()



class EvangelismPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(EvangelismType)
