import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import Blog,Comments,Tags,Category


class BlogType(DjangoObjectType):
    """
    Create a GraphQL type for the blog model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Blog

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()




class BlogInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    title = graphene.String()
    post = graphene.String()
    summary = graphene.String()
    published = graphene.Date()
    category = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    comments = graphene.String()
    author = graphene.String()
    status = graphene.String()


class BlogPaginatedType(graphene.ObjectType):
    """
    Blog pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(BlogType)


class CommentType(DjangoObjectType):
    """
    Create a GraphQL type for the comment model
    """
    history = graphene.List(GenericScalar)
    status = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Comments

    def resolve_history(self, info):
        return get_history(self)

    def resolve_status(self, *args):
        return self.get_status_display()




class CommentInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    title = graphene.String()
    content = graphene.String()
    creator = graphene.String()
    status = graphene.String()
    blog = graphene.String()


class CommentPaginatedType(graphene.ObjectType):
    """
    Blog pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(CommentType)


class CategoryType(DjangoObjectType):
    """
    Create a GraphQL type for the category model
    """
    history = graphene.List(GenericScalar)

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Category

    def resolve_history(self, info):
        return get_history(self)


class CategoryInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    title = graphene.String()
    content = graphene.String()


class CategoryPaginatedType(graphene.ObjectType):
    """
    Blog pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(CategoryType)


class TagsType(DjangoObjectType):
    """
    Create a GraphQL type for the category model
    """
    history = graphene.List(GenericScalar)

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Tags

    def resolve_history(self, info):
        return get_history(self)


class TagsInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    title = graphene.String()
    content = graphene.String()


class TagsPaginatedType(graphene.ObjectType):
    """
    Blog pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(TagsType)


