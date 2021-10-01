from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from app.api.authentication.models import User


class Tags(BaseModel):
    name = models.CharField(max_length=255)


class Category(BaseModel):
    name = models.CharField(max_length=255)


class Author(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class Publisher(BaseModel):
    name = models.CharField(max_length=255)

class Book(BaseModel):
    name = models.TextField()
    isbn = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,
    null=True,blank=True)
    author = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Category)
    published = models.DateField()

    def __str__(self):
        return self.name


class Premium(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True,blank=True)
    paid = models.BooleanField(default=False)
    content = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
