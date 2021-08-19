import graphene

from app.api.authentication.mutations import Mutation as auth_mutation
from app.api.authentication.query import Query as user_query


class Query(user_query, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


class Mutation(auth_mutation, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
