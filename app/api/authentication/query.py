import graphene
from django.db.models import Q
from graphene_django.types import ObjectType
from graphql_extensions.auth.decorators import login_required

from ..helpers.pagination_helper import pagination_helper
from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from .helpers.user_helpers import get_roles
from ..helpers.validate_object_id import validate_object_id
from .models import User
from .object_types import UsersPaginatedType, UserType
from .validators.validate_input import UserValidations
from graphene.types.generic import GenericScalar


class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.String())
    profile = graphene.Field(UserType)
    users = graphene.Field(UsersPaginatedType,
                           search=graphene.String(),
                           page=graphene.Int(),
                           limit=graphene.Int(),
                           is_staff=graphene.Boolean())
    roles = graphene.List(graphene.String)
    role_permissions = graphene.Field(GenericScalar, role=graphene.String())

    @token_required
    @login_required
    def resolve_user(self, info, **kwargs):
        error_msg = error_dict['permission_denied'].format("view", 'user')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        return validate_object_id(id, User, "user", info.context.user.agency)

    @token_required
    @login_required
    def resolve_users(self, info, search=None, is_staff=False, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        error_msg = error_dict['admin_only'].format('list users')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        if search:
            filter = (
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )
            users = User.objects.filter(
                filter,username=info.context.user.username).all()
        else:
            users = User.objects.filter(username=info.context.user.username).all()
            if is_staff:
                users = users.filter(is_staff=True)
        users = users.order_by('first_name')
        return pagination_helper(users, page, limit, UsersPaginatedType)

    @token_required
    @login_required
    def resolve_profile(self, info, **kwargs):
        return info.context.user

    @token_required
    @login_required
    def resolve_roles(self, info, **kwargs):
        available_roles = get_roles()
        return available_roles

    @token_required
    @login_required
    def resolve_role_permissions(self, info, **kwargs):
        validator = UserValidations()
        available_permissions = validator.validate_user_role(
            kwargs.get("role", '').strip())
        return available_permissions
