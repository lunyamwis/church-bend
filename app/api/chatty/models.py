from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from app.api.authentication.models import User


class Group(BaseModel):
    name = models.CharField(max_length=255)


class Thread(BaseModel):
    name = models.CharField(max_length=255)

class Chat(BaseModel):

    class ChatOptions(models.TextChoices):
        NORMAL = 'N',_('Normal')
        WHATSAPP = 'W',_('Whatsapp')
        EMAIL = 'E',_('Email')

    delivered = models.BooleanField()
    read = models.BooleanField()
    text = models.TextField()
    response = models.TextField()
    email = models.TextField()
    sms = models.TextField()
    chat_type = models.CharField(max_length=50,
    choices=ChatOptions.choices,default=ChatOptions.NORMAL)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,null=True,blank=True)
    group = models.ManyToManyField(Group)

