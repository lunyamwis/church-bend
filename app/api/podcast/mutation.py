import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Podcast,Tags,Category,Premium
)
from .validators.validate_input import PodcastValidations
from .object_types import (
    PodcastInput,PodcastType,
    PodcastCategoryInput,PodcastCategoryType,
    PodcastTagsType, PodcastTagsInput,
    PodcastPremiumType,PodcastPremiumInput
)
from datetime import datetime


class CreatePodcast(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    podcast = graphene.Field(PodcastType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = PodcastInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a podcast")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = PodcastValidations()
        data = validator.validate_podcast_data(
            kwargs.get("input", ''))
        tags = data.pop("tags", [])
        categories = data.pop("categories",[])
        new_podcast = Podcast(**data)
        new_podcast.save()
        for tag in tags:
            tag_ = Tags.objects.get(id=tag)
            new_podcast.tags.add(tag_)
        for category in categories:
            category_ = Category.objects.get(id=category)
            new_podcast.categories.add(category_)
        return CreatePodcast(status="Success", podcast=new_podcast,
                                      message=SUCCESS_ACTION.format("Podcast created"))

class CreatePremiumPodcasts(graphene.Mutation):
    '''Handle addition of a podcast and handle saving it to the db'''
    # items that the mutation will return
    premium_podcast = graphene.Field(PodcastPremiumType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the podcast creation'''
        input = PodcastPremiumInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("Add Premium podcasts")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = PodcastValidations()
        data = validator.validate_premium_podcast_data(
            kwargs.get("input", ''))
        podcasts = data.pop("content",[])
        new_premium_podcast = Premium(**data)
        new_premium_podcast.save()
        for podcast in podcasts:
            podcast_ = podcast(**podcast)
            new_premium_podcast.content.add(podcast_)
        return CreatePremiumPodcasts(status="Success", premium_podcast=new_premium_podcast,
                                    message=SUCCESS_ACTION.format("Premium podcasts added"))

class Mutation(graphene.ObjectType):
    create_podcast = CreatePodcast.Field()
    create_premium_podcasts = CreatePremiumPodcasts.Field()