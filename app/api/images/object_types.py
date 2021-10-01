import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import (
    Category,
    Images,Tags,Premium
)


class ImageTagsType(DjangoObjectType):
    """
    creates a graphql type for the Tags Model
    """
    class Meta:
        model = Tags


class ImageCategoryType(DjangoObjectType):
    """
    creates a graphql type for the Category model
    """
    class Meta:
        model = Category

class ImageCategoryInput(graphene.InputObjectType):
    name = graphene.String()

class ImageTagsInput(graphene.InputObjectType):
    name = graphene.String()

class ImageType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Images

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()



class ImagesInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()
    description = graphene.String()
    tags = graphene.List(ImageTagsInput)
    categories = graphene.List(ImageCategoryInput)
    image = graphene.String()
    
class ImagePaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(ImageType)



class ImagePremiumType(DjangoObjectType):
    class Meta:
        model=Premium

class ImagePremiumInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    paid = graphene.Boolean()
    content = graphene.List(ImagesInput)

class PremiumImagePaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(ImagePremiumType)