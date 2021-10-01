from django.db import models
from app.api.models import BaseModel
from django.contrib.postgres.fields import ArrayField


class Member(BaseModel):
    conference_name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    home_church_name = models.TextField()
    home_church_email = models.EmailField(max_length=254)
    home_church_phone_numbers = models.CharField(max_length=200,null=True)
    home_church_location = models.CharField(max_length=50)
    church_elder_first_name = models.CharField(max_length=50)
    church_elder_last_name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=255)
    baptized = models.BooleanField(default=True)
    position_church = models.CharField(max_length=255)

    def __str__(self):
        return self.home_church_name

