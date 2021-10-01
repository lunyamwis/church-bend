import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Images,Tags,Category,Premium
)

from .validators.validate_input import ImageValidations
from .object_types import (
    ImageCategoryInput,ImageCategoryType,
    ImageTagsInput,ImageTagsType,
    ImagesInput,ImageType,
    ImagePremiumType,ImagePremiumInput
)
from datetime import datetime


class CreateImages(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    image = graphene.Field(ImageType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = ImagesInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a image")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = ImageValidations()
        data = validator.validate_image_data(
            kwargs.get("input", ''))
        tags = data.pop("tags",[])
        categories = data.pop("categories",[])
        new_image = Images(**data)
        new_image.save()
        for tag in tags:
            tag_ = Tags.objects.get(id=tag)
            new_image.tags.add(tag_)
        for category in categories:
            category_ = Category.objects.get(id=category)
            new_image.categories.add(category_)
        return CreateImages(status="Success", image=new_image,
                                    message=SUCCESS_ACTION.format("Image created"))


class CreatePremiumImages(graphene.Mutation):
    '''Handle addition of a book and handle saving it to the db'''
    # items that the mutation will return
    premium_image = graphene.Field(ImagePremiumType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the book creation'''
        input = ImagePremiumInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("Add Premium Image")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = ImageValidations()
        data = validator.validate_premium_image_data(
            kwargs.get("input", ''))
        images = data.pop("content",[])
        new_premium_image = Premium(**data)
        new_premium_image.save()
        for image in images:
            image_ = Images(**image)
            new_premium_image.content.add(image_)
        return CreatePremiumImages(status="Success", premium_image=new_premium_image,
                                    message=SUCCESS_ACTION.format("Premium Images added"))



class Mutation(graphene.ObjectType):
    create_images = CreateImages.Field()
    create_premium_images = CreatePremiumImages.Field()