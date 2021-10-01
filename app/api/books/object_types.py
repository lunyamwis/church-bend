import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import (
    Author,
    Book,Category,Tags,Publisher,Premium
)




class PublisherType(DjangoObjectType):
    """
    creates a graphql type for the publisher model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        model=Publisher

    def resolve_history(self,info):
        return get_history(self)

    def resolve_status(self,*args):
        return self.get_status_display()



class AuthorType(DjangoObjectType):
    """
    Creates a graphql type for the author model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        model=Author

    def resolve_history(self,info):
        return get_history(self)

    def resolve_status(self,*args):
        return self.get_status_display()


class BookTagsType(DjangoObjectType):
    """
    Creates a graphql type for the tags model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        model=Tags

    def resolve_history(self,info):
        return get_history(self)

    def resolve_status(self,*args):
        return self.get_status_display()


class BookCategoryType(DjangoObjectType):
    """
    Creates a graphql type for the category model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        model = Category

    def resolve_history(self,info):
        return get_history(self)

    def resolve_status(self,*args):
        return self.get_status_display()


class BookType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Book

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()

class PublisherInput(graphene.InputObjectType):
    name = graphene.String()

class AuthorInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()

class BookTagsInput(graphene.InputObjectType):
    name = graphene.String()

class BookCategoryInput(graphene.InputObjectType):
    name = graphene.String()



class BookInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()
    isbn = graphene.String()
    publisher = graphene.String()
    author = graphene.List(AuthorInput)
    tags = graphene.List(BookTagsInput)
    categories = graphene.List(BookCategoryInput)
    published = graphene.Date()

class BookPremiumType(DjangoObjectType):
    class Meta:
        model=Premium

class BookPremiumInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Float()
    paid = graphene.Boolean()
    content = graphene.List(BookInput)

class PremiumBookPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(BookPremiumType)




class BookPaginatedType(graphene.ObjectType):
    """
    Individual Client pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(BookType)


