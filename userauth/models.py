from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserData(models.Model):
    author = models.CharField(max_length=20,unique = True)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return self.user_type
