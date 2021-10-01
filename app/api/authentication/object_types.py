import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType
from rolepermissions.roles import get_user_roles
from ..member.object_types import (
    MemberInput,MemberType
)
from ..minister.object_types import(
    MinisterInput,MinisterType
)
from ..ministry.object_types import (
    MinistryInput,MinistryType
)

from .models import User


class UserType(DjangoObjectType):
    """
    Create a GraphQL type for the user model
    """
    description = " Type definition for a single user "
    roles = graphene.List(graphene.String)
    order_by = OrderingFilter(fields=(
        ('username', 'first_name'),
    ))

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = User
        exclude_fields = ('password',)

    def resolve_roles(self, info):
        """
        Get the user role
        Args:
            self (obj): current model reference
            info (obj): metadata
        Return:
            roles (list): user roles
        """
        roles_ = get_user_roles(self)
        roles = [role.get_name() for role in roles_ if roles_]
        return roles



class AdminType(UserType):

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = User
        exclude_fields = ('password',)


class PasswordResetInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    email = graphene.String(required=True)


class UserInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    username = graphene.String()
    password = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    image = graphene.String()
    member = graphene.List(MemberInput)
    minister = graphene.List(MinisterInput)
    ministry = graphene.List(MinistryInput)
    

class UserUpdateInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    username = graphene.String()
    password = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    image = graphene.String()


# Now we create a corresponding PaginatedType for that object type:
class UsersPaginatedType(graphene.ObjectType):
    """
    User pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(UserType)
