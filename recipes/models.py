# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
import timedelta

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    preparation_time = timedelta.fields.TimedeltaField(null=True, blank=True)
    baking_time = timedelta.fields.TimedeltaField(null=True, blank=True)
    baking_temperature = models.CommaSeparatedIntegerField(max_length=20, 
                                                           null=True,
                                                           blank=True)
    portion = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, editable=False)
    calory = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=42, blank=True)
    small_picture = models.ImageField(upload_to='media', null=True, blank=True)
    big_picture = models.ImageField(upload_to='media', null=True, blank=True)
    hint = models.TextField(blank=True)
    ingredients = models.TextField()
    content = models.TextField()
    category = models.ForeignKey('Category')
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que nous
        traiterons plus tard et dans l'administration
        """
        return self.title
    
    def __unicode__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que nous
        traiterons plus tard et dans l'administration
        """
        return u"%s" % self.title
