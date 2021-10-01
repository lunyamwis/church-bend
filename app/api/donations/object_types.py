import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from ..history.views import get_history
from .models import Donations


class DonationType(DjangoObjectType):
    """
    Create a GraphQL type for the client model
    """
    history = graphene.List(GenericScalar)
    donation_type = graphene.String()

    class Meta:
        '''Defines the fields to be serialized in the user model'''
        model = Donations

    def resolve_history(self, info):
        return get_history(self)

    def resolve_donation_type(self, *args):
        return self.get_donation_type_display()



class DonationInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    first_name = graphene.String()
    last_name = graphene.String()
    donation_type = graphene.String()
    amount = graphene.Float()
    notes = graphene.String()
    ministry = graphene.String()
    minister = graphene.String()
    monthly = graphene.Boolean()

class CorporateClientInput(graphene.InputObjectType):
    """
    Create Input Object Types
    """
    name = graphene.String()
    about = graphene.String()
    email = graphene.String()
    kra_pin = graphene.String()
    phone_number = graphene.String()
    postal_address = graphene.String()
    town = graphene.String()
    contact_persons = graphene.List(graphene.String)
    facebook_account = graphene.String()
    twitter_account = graphene.String()
    instagram_account = graphene.String()
    linkedin_account = graphene.String()
    status = graphene.String()


