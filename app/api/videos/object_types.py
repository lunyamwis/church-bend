import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import (Video,Tags,Categories,Premium)


class VideoType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Video

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()


class VideoInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    title = graphene.String()
    description = graphene.String()
    tags = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)
    video = graphene.String()

class VideoPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(VideoType)



class VideoTagsType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Tags



class VideoTagsInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()

class TagsPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(VideoTagsType)




class VideoCategoryType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Categories


class VideoCategoryInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()

class CategoryPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(VideoCategoryType)
    


class VideoPremiumType(DjangoObjectType):
    class Meta:
        model=Premium

class VideoPremiumInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    paid = graphene.Boolean()
    content = graphene.List(VideoInput)

class PremiumVideoPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()

