from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from userauth.models import UserData


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.CharField(max_length=30)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


# class UserData(models.Model):
#     author = models.CharField(max_length=20,unique = True)
#     user_type = models.CharField(max_length=20)

#     def __str__(self):
#         return self.user_type
#     class Meta:
#         db_table = 'userauth_UserData'