import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validate_object_id import validate_object_id
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from ..authentication.models import User
from .models import (
    Blog, Category, Comments, Tags
)
from .validators.validate_input import BlogValidations
from .object_types import (
    BlogInput, BlogType, CategoryInput, CategoryType,
    CommentInput, CommentType, TagsInput, TagsType
)
from datetime import datetime


class CreateBlog(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    blog = graphene.Field(BlogType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = BlogInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a blog")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = BlogValidations()
        data = validator.validate_blog_data(
            kwargs.get("input", ''))
        categories = data.pop('category', [])
        tags = data.pop('tags', [])
        new_blog = Blog(**data)
        new_blog.is_active = True
        new_blog.save()
        for category in categories:
            category_ = Category.objects.get(id=category)
            new_blog.category.add(category_)
        for tag in tags:
            tag_ = Tags.objects.get(id=tag)
            new_blog.tags.add(tag_)
        return CreateBlog(status="Success", blog=new_blog,
                        message=SUCCESS_ACTION.format("Blog created"))

class UpdateBlog(graphene.Mutation):
    """
    handles updating of books
    """

    blog = graphene.Field(BlogType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = BlogInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a blog')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        blog_update = validate_object_id(id,Blog,"Blog")
        data = kwargs['input']
        if data['author']:
            data['author'] = validate_object_id(
                data['author'], User,
                "Author")

        tags = data.pop('tags',[])
        categories = data.pop('category',[])
        for tag in tags:
            add_tag = Tags(**tag)
            add_tag.save()
            blog_update.tags.add(add_tag)
        for category in categories:
            add_category = Category(**category)
            add_category.save()
            blog_update.category.add(add_category)
        for (key,value) in data.items():
            setattr(blog_update,key,value)
        blog_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Blog Entry has been updated")

        return UpdateBlog(status = status,blog=blog_update,message=message)



class CreateComment(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    comment = graphene.Field(CommentType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = CommentInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a comment")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = BlogValidations()
        data = validator.validate_comment_data(
            kwargs.get("input", ''))
        new_comment = Comments(**data)
        new_comment.save()
        return CreateComment(status="Success", comment=new_comment,
                        message=SUCCESS_ACTION.format("Comment created"))


class UpdateComment(graphene.Mutation):
    """
    handles updating of books
    """

    comment = graphene.Field(CommentType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = CommentInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a comment')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        comment_update = validate_object_id(id,Comments,"Comment")
        data = kwargs['input']
        if data['blog']:
            data['blog'] = validate_object_id(
                data['blog'], Blog,
                "blog")

        if data['creator']:
            data['creator'] = validate_object_id(
                data['creator'],User,"creator"
            )

        for (key,value) in data.items():
            setattr(comment_update,key,value)
        comment_update.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Comment has been updated")

        return UpdateComment(status = status,comment=comment_update,message=message)


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    create_comment = CreateComment.Field()
    update_blog = UpdateBlog.Field()
    update_comment = UpdateComment.Field()
