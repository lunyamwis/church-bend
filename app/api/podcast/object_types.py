import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType
from ..history.views import get_history
from .models import (Podcast,Tags,Category,Premium)



class PodcastTagsType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Tags


class PodcastTagsInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()

class PodcastCategoryType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Category



class PodcastCategoryInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()



class PodcastType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Podcast

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()


class PodcastInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()
    sort_by_date = graphene.Boolean()
    podcast_type = graphene.String()
    duration = graphene.String()
    published = graphene.Date()
    language = graphene.String()
    region = graphene.String()
    podcast = graphene.String()

class PodcastPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(PodcastType)



class PodcastPremiumType(DjangoObjectType):
    class Meta:
        model=Premium

class PodcastPremiumInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    paid = graphene.Boolean()
    content = graphene.List(PodcastInput)

class PremiumPodcastPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(PodcastPremiumType)