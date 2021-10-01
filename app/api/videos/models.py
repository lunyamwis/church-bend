from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField

class Tags(BaseModel):
    name = models.CharField(max_length=255)


class Categories(BaseModel):
    name = models.CharField(max_length=255)


class Video(BaseModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Categories)
    video = models.URLField()


    def __str__(self):
        return self.title


class Premium(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True,blank=True)
    paid = models.BooleanField(default=False)
    content = models.ManyToManyField(Video)

    def __str__(self):
        return self.name