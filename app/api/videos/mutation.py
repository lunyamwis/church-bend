import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Video,Tags,Categories,Premium
)
from .validators.validate_input import VideoValidations
from .object_types import (
    Video,VideoType,VideoInput,
    VideoTagsType,VideoCategoryType,
    VideoPremiumType,VideoPremiumInput
)
from datetime import datetime


class CreateVideo(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    video = graphene.Field(VideoType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = VideoInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a video")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = VideoValidations()
        data = validator.validate_video_data(
            kwargs.get("input", ''))
        tags = data.pop("tags", [])
        categories = data.pop("categories",[])
        new_video = Video(**data)
        new_video.save()
        for tag in tags:
            tag_ = Tags.objects.get(id=tag)
            new_video.tags.add(tag_)
        for category in categories:
            category_ = Categories.objects.get(id=category)
            new_video.tags.add(category_)
        return CreateVideo(status="Success", video=new_video,
                                    message=SUCCESS_ACTION.format("Video created"))

class CreatePremiumVideos(graphene.Mutation):
    '''Handle addition of a video and handle saving it to the db'''
    # items that the mutation will return
    premium_videos = graphene.Field(VideoPremiumType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the video creation'''
        input = VideoPremiumInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("Add Premium videos")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = VideoValidations()
        data = validator.validate_premium_videos_data(
            kwargs.get("input", ''))
        videos = data.pop("content",[])
        new_premium_videos = Premium(**data)
        new_premium_videos.save()
        for video in videos:
            video_ = video(**video)
            new_premium_videos.content.add(video_)
        return CreatePremiumVideos(status="Success", premium_videos=new_premium_videos,
                                    message=SUCCESS_ACTION.format("Premium videos added"))

class Mutation(graphene.ObjectType):
    create_video = CreateVideo.Field()
    create_premium_videos = CreatePremiumVideos.Field()