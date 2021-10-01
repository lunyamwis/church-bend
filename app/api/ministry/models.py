from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.evangelism.models import Evangelism
from app.api.minister.models import Minister
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField


class Ministry(BaseModel):
    class TypeOptions(models.TextChoices):
        INDEPENDENT = 'I',_('Self Supporting')
        CHURCHBASED = 'C',_('Supported Church')

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_numbers = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=50,choices=TypeOptions.choices,
                                default=TypeOptions.INDEPENDENT)
    conference_name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Evangelism)
    home_church_name = models.TextField()
    home_church_email = models.EmailField(max_length=254)
    home_church_phone_numbers = models.CharField(max_length=200,null=True)
    home_church_location = models.CharField(max_length=50)
    church_elder_first_name = models.CharField(max_length=50)
    church_elder_last_name = models.CharField(max_length=50)


    def __str__(self):
        return self.name