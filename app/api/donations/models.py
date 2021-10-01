from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.ministry.models import Ministry
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField

class Donations(BaseModel):
    class TypeOptions(models.TextChoices):
        SPECIAL_NEEDS = 'S',_('Special Needs')
        MINISTER_SUPPORT = 'MS',_('Support Minister')
        MINISTRY_SUPPORT = 'MIS',_('Support a Ministry')
        LAYLINKS = 'L',_('Laylinks')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    donation_type = models.CharField(max_length=50,choices=TypeOptions.choices,
    default=TypeOptions.SPECIAL_NEEDS)
    amount = models.IntegerField()
    notes = models.TextField()
    ministry = models.ForeignKey(Ministry,on_delete=models.CASCADE,
                                null=True,blank=True) 
    minister = models.ForeignKey(Minister,on_delete=models.CASCADE,
                                null=True,blank=True) 
    monthly = models.BooleanField()

    def __str__(self):
        return self.first_name