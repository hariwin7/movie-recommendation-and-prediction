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

class Ratings(models.Model):
    userid = models.IntegerField(default=0)
    movieid = models.IntegerField(default=0)
    rating =  models.IntegerField(default=0)

class Director(models.Model):
    dirname = models.CharField(max_length=30 , default='')
    dir_avg_profit = models.FloatField()
    dir_no_movies = models.IntegerField()

class Actorone(models.Model):
    act_1_name = models.CharField(max_length=30 , default='')
    act_1_avg_profit = models.FloatField()
    act_1_no_movies = models.IntegerField()

class Actortwo(models.Model):
    act_2_name = models.CharField(max_length=30 , default='')
    act_2_avg_profit = models.FloatField()
    act_2_no_movies = models.IntegerField()

class Actorthree(models.Model):
    act_3_name = models.CharField(max_length=30 , default='')
    act_3_avg_profit = models.FloatField()
    act_3_no_movies = models.IntegerField()
