from django.db import models
from app.api.models import BaseModel
from app.api.evangelism.models import Evangelism
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Minister(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    email = models.EmailField()
    contact_assistant_name = models.CharField(max_length=255)
    contact_assistant_email = models.EmailField()
    conference_name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Evangelism)
    home_church_name = models.TextField()
    home_church_email = models.EmailField(max_length=254)
    home_church_phone_numbers = models.CharField(max_length=200,null=True)
    home_church_location = models.CharField(max_length=50)
    church_elder_first_name = models.CharField(max_length=50)
    church_elder_last_name = models.CharField(max_length=50)
    
