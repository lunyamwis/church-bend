from django.db import models
from app.api.models import BaseModel
from django.utils.translation import gettext_lazy as _
from app.api.minister.models import Minister
from app.api.evangelism.models import Evangelism
from app.api.member.models import Member
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from app.api.authentication.models import User


class Category(BaseModel):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)




class Tags(BaseModel):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)


class Blog(BaseModel):
    class BlogOptions(models.TextChoices):
        PUBLISHED = 'P', _('Published')
        DRAFT = 'D', _('Draft')

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=BlogOptions.choices,
                              default=BlogOptions.DRAFT)
    post = models.TextField()
    summary = models.TextField()
    published = models.DateField()
    category = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                               blank=True)
    
    def __str__(self):
        return self.title


class Comments(BaseModel):
    class CommentOptions(models.TextChoices):
        APPROVED = 'A', _('Approved')
        DECLINED = 'D', _('Declined')

    title = models.CharField(max_length=255)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    status = models.CharField(max_length=50, choices=CommentOptions.choices,
                              default=CommentOptions.APPROVED)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                                 null=True, blank=True)
    def __str__(self):
        return self.title
