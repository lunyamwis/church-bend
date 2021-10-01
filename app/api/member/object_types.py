import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import Member


class MemberType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Member

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()



class MemberInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    conference_name = graphene.String()
    field_name = graphene.String()
    home_church_name = graphene.String()
    home_church_email = graphene.String()
    home_church_phone_numbers = graphene.String()
    home_church_location = graphene.String()
    church_elder_first_name = graphene.String()
    church_elder_last_name = graphene.String()
    occupation = graphene.String()
    baptized = graphene.Boolean()
    position_church = graphene.String()
    

class MemberPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(MemberType)
