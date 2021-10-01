import graphene

from app.api.authentication.mutations import Mutation as auth_mutation
from app.api.blog.mutation import Mutation as blog_mutation
from app.api.donations.mutation import Mutation as donation_mutation
from app.api.books.mutation import Mutation as book_mutation
from app.api.evangelism.mutation import Mutation as evangelism_mutation
from app.api.images.mutation import Mutation as image_mutation
from app.api.member.mutation import Mutation as member_mutation
from app.api.minister.mutation import Mutation as minister_mutation
from app.api.ministry.mutation import Mutation as ministry_mutation
from app.api.podcast.mutation import Mutation as podcast_mutation
from app.api.videos.mutation import Mutation as video_mutation
from app.api.chatty.mutation import Mutation as chat_mutation
from app.api.authentication.query import Query as user_query


class Query(user_query, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


class Mutation(auth_mutation, blog_mutation,
                donation_mutation,book_mutation,
                evangelism_mutation,image_mutation,
                member_mutation, minister_mutation,
                ministry_mutation,podcast_mutation,
                chat_mutation, video_mutation,
                graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
