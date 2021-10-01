from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Tags(BaseModel):
    name = models.CharField(max_length=255)


class Category(BaseModel):
    name = models.CharField(max_length=255)



class Podcast(BaseModel):

    class TypeOptions(models.TextChoices):
        EPISODE = 'E',_('Episode')
        SERIES = 'S',_('Series')

    class LanguageOptions(models.TextChoices):
        KISWAHILI = 'K',_('Kiswahili')
        ENGLISH = 'E',_('English')

    name = models.CharField(max_length=255)
    sort_by_date = models.BooleanField()
    podcast_type = models.CharField(max_length=255,choices=TypeOptions.choices,
                                    default=TypeOptions.EPISODE)
    duration = models.CharField(max_length=255)
    published = models.DateField()
    language = models.CharField(max_length=500,choices=LanguageOptions.choices,
                                default=LanguageOptions.ENGLISH)
    region = models.CharField(max_length =255)
    podcast = models.URLField()
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Category)


    def __str__(self):
        return self.name
        

class Premium(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True,blank=True)
    paid = models.BooleanField(default=False)
    content = models.ManyToManyField(Podcast)

    def __str__(self):
        return self.name