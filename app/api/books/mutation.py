import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validate_object_id import validate_object_id
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Tags,
    Author,
    Book,
    Category,
    Publisher,
    Premium
)
from .validators.validate_input import BookValidations
from .object_types import (
    BookInput,BookType,
    AuthorType,AuthorInput,
    BookTagsType,BookTagsInput,
    BookCategoryType,BookCategoryInput,
    PublisherInput,PublisherType,
    BookPremiumType,BookPremiumInput
)
from datetime import datetime


class CreateBook(graphene.Mutation):
    '''Handle addition of a book and handle saving it to the db'''
    # items that the mutation will return
    book = graphene.Field(BookType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the book creation'''
        input = BookInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("Add a Book")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = BookValidations()
        data = validator.validate_book_data(
            kwargs.get("input", ''))
        authors = data.pop("author", [])
        tags = data.pop("tags",[])
        categories = data.pop("categories",[])
        new_book = Book(**data)
        new_book.save()
        for author in authors:
            author_ = Author.objects.get(id=author)
            new_book.author.add(author_)
        for tag in tags:
            tag_ = Tags.objects.get(id=tag)
            new_book.tags.add(tag_)
        for category in categories:
            category_ = Category.objects.get(id=category)
            new_book.categories.add(category_)

        return CreateBook(status="Success", book=new_book,
                                    message=SUCCESS_ACTION.format("Book added"))

class UpdateBook(graphene.Mutation):
    """
    handles updating of books
    """

    book_val = graphene.Field(BookType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = BookInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a book')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        book = validate_object_id(id,Book,"Book")
        data = kwargs['input']
        tags = data.pop('tags',[])
        categories = data.pop('categories',[])
        for tag in tags:
            add_tag = Tags(**tag)
            add_tag.save()
            book.tags.add(add_tag)
        for category in categories:
            add_category = Category(**category)
            add_category.save()
            book.categories.add(add_category)
        for (key,value) in data.items():
            setattr(book,key,value)
        book.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Book Entry has been updated")

        return UpdateBook(status = status,book_val=book,message=message)

class CreatePremiumBooks(graphene.Mutation):
    '''Handle addition of a book and handle saving it to the db'''
    # items that the mutation will return
    premium_book = graphene.Field(BookPremiumType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the book creation'''
        input = BookPremiumInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("Add Premium Books")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = BookValidations()
        data = validator.validate_premium_book_data(
            kwargs.get("input", ''))
        books = data.pop("content",[])
        new_premium_book = Premium(**data)
        new_premium_book.save()
        for book in books:
            book_ = Book(**book)
            new_book.content.add(book_)
        return CreatePremiumBooks(status="Success", premium_book=new_premium_book,
                                    message=SUCCESS_ACTION.format("Premium Books added"))

class UpdatePremiumBook(graphene.Mutation):
    """
    handles updating of books
    """

    premium_book_set = graphene.Field(BookPremiumType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = BookPremiumInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update a premium book')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        premium_book = validate_object_id(id,Premium,"Premium")
        data = kwargs['input']
        books = data.pop('content',[])
        for book in books:
            add_book = Book(**book)
            add_book.save()
            premium_book.content.add(add_book)
        for (key,value) in data.items():
            setattr(premium_book,key,value)
        premium_book.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Premium Book Entry has been updated")

        return UpdatePremiumBook(status = status,premium_book_set=premium_book,message=message)



class CreatePulisher(graphene.Mutation):

    """
    handles addition of new Publisher
    """
    publisher = graphene.Field(PublisherType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the publisher creation'''
        input = PublisherInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Add a Publisher")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        data = kwargs['input']
        new_publisher = Publisher(**data)
        new_publisher.save()

        return CreatePulisher(status="Success", publisher=new_publisher,
                                    message=SUCCESS_ACTION.format("Publisher added"))


class UpdatePublisher(graphene.Mutation):
    """
    handles updating of books
    """

    publisher_entry = graphene.Field(PublisherType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = PublisherInput(required=True)
        id = graphene.String(required=True)
    
    @staticmethod
    @token_required
    @login_required
    def mutate(root,info,**kwargs):
        error_msg=error_dict['admin_only'].format('update publisher')
        role_required(info.context.user,['admin','manager'],error_msg)
        id = kwargs.get('id',None)
        publisher = validate_object_id(id,Publisher,"Publisher")
        data = kwargs['input']
        for (key,value) in data.items():
            setattr(publisher,key,value)
        publisher.save()
        status = "Success"
        message = SUCCESS_ACTION.format("Publisher has been updated")

        return UpdatePublisher(status = status,publisher_entry=publisher,message=message)




class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    create_premium_books = CreatePremiumBooks.Field()
    create_publisher = CreatePulisher.Field()
    update_book = UpdateBook.Field()    
    update_premium_book = UpdatePremiumBook.Field()
    update_publisher = UpdatePublisher.Field()
    