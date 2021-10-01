from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Evangelism(BaseModel):
    class FieldOptions(models.TextChoices):
        PREACHER = 'PR',_('Preacher')
        PROPHECY = 'P',_('Prophecy')
        MEDICAL = 'M',_('Medical')
        PERSONAL = 'PE',_('Personal Evangelism')
        CHILD = 'CH',_('Child Evangelism')
        SONG = 'SO',_('Song Evangelism')
        CITY = 'C',_('City Evangelism')
        DISABLED = 'D',_('Disability Evangelism')
        SPECIAL = 'S',_('Special Classes Evangelism')
        BIBLESTUDY = 'BS',_('Bible Study Evangelism')
        PUBLISHING = 'PU',_('Publishing Evangelism')
        LAY = 'L',_('Lay Evangelism')   

    class EventOptions(models.TextChoices):
        HEALTHEXPO = 'HE',_('Health Expo')
        PERSONAL = 'P',_('Personal')
        PUBLIC = 'PU',_('Public Effort')
        MEETING = 'M',_('Hall Meetings')
        LIVESTREAM = 'L',_('Live Streaming')
        RECORDED = 'R',_('Recorded Message')
        MATERIAL = 'MD',_('Printed Material Distribution')
        SERMON = 'S',_('Sermon')

    field = models.CharField(max_length=50,choices=FieldOptions.choices,
                            default=FieldOptions.PERSONAL)
    event = models.CharField(max_length=50,choices=EventOptions.choices,
                            default=EventOptions.PERSONAL)
    event_name = models.TextField(max_length=1024)
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=255)
    event_purpose = models.TextField()
    event_duration = models.CharField(max_length=1024)
    sermon_theme = models.TextField()
    sermon_length = models.IntegerField()
    number_attendees = models.IntegerField()
    budget = models.FloatField()
    number_converts = models.IntegerField()
    number_followups = models.IntegerField()

    def __str__(self):
        return self.field