from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserProfile(models.Model):
    userid = models.IntegerField(default=0)
    username = models.CharField(max_length=30 , default='')
    password = models.CharField(max_length=30 , default='')

class Movie(models.Model):
    movieid = models.IntegerField(default=0)
    moviename = models.CharField(max_length=30 , default='')
    genre = models.CharField(max_length=30 , default='')
