import graphene
from app.api.client.helpers.client_helpers import get_default_client_status
from django.db.models import Q
from graphene.types.generic import GenericScalar
from graphene_django.types import ObjectType
from graphql_extensions.auth.decorators import login_required

from ..helpers.pagination_helper import pagination_helper
from ..helpers.permission_required import role_required, token_required
from ..helpers.validate_object_id import validate_object_id
from ..helpers.validation_errors import error_dict
from .models import CorporateClient, IndividualClient
from .object_types import (CorporateClientPaginatedType, CorporateClientType,
                           IndividualClientPaginatedType, IndividualClientType)


class Query(ObjectType):
    client_status_options = GenericScalar()
    individual_client = graphene.Field(IndividualClientType, id=graphene.String())
    corporate_client = graphene.Field(CorporateClientType, id=graphene.String())
    individual_clients = graphene.Field(IndividualClientPaginatedType,
                                        page=graphene.Int(),
                                        search=graphene.String(),
                                        limit=graphene.Int())
    corporate_clients = graphene.Field(CorporateClientPaginatedType,
                                       page=graphene.Int(),
                                       search=graphene.String(),
                                       limit=graphene.Int())

    @token_required
    @login_required
    def resolve_client_status_options(self, info, **kwargs):
        return get_default_client_status()

    @token_required
    @login_required
    def resolve_individual_client(self, info, **kwargs):
        error_msg = error_dict['permission_denied'].format("view", 'client')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        return validate_object_id(id, IndividualClient,
                                  "Individual Client", info.context.user.agency)

    @token_required
    @login_required
    def resolve_corporate_client(self, info, **kwargs):
        error_msg = error_dict['permission_denied'].format("view", 'client')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        return validate_object_id(id, CorporateClient,
                                  "Corporate Client", info.context.user.agency)

    @token_required
    @login_required
    def resolve_corporate_clients(self, info, search=None, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        error_msg = error_dict['admin_only'].format('list clients')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        if search:
            filter = (
                Q(name__icontains=search) |
                Q(about__icontains=search) |
                Q(postal_address__icontains=search) |
                Q(kra_pin__icontains=search) |
                Q(town__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(status__icontains=search)
            )
            clients = CorporateClient.objects.filter(
                filter, agency=info.context.user.agency).all().order_by(
                    'name')
        else:
            clients = CorporateClient.objects.filter(
                agency=info.context.user.agency).all().order_by(
                    'name')
        return pagination_helper(clients, page, limit, CorporateClientPaginatedType)

    @token_required
    @login_required
    def resolve_individual_clients(self, info, search=None, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        error_msg = error_dict['admin_only'].format('list clients')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        if search:
            filter = (
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(postal_address__icontains=search) |
                Q(surname__icontains=search) |
                Q(kra_pin__icontains=search) |
                Q(town__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(status__icontains=search)
            )
            clients = IndividualClient.objects.filter(
                filter, agency=info.context.user.agency).all().order_by(
                    'first_name')
        else:
            clients = IndividualClient.objects.filter(
                agency=info.context.user.agency).all().order_by(
                    'first_name')
        return pagination_helper(clients, page, limit, IndividualClientPaginatedType)
