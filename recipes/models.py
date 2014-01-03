# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

import datetime

import timedelta
from stdimage import StdImageField

from slugify import unique_slugify

class Source(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)
    url = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]
        
    def __unicode__(self):
        return self.name
        
    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(Source, self).save()

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name
    
    def save(self, **kwargs):
        unique_slugify(self, self.name)
        super(Category, self).save()

class Recipe(models.Model):
    DIFFICULTY_CHOICES = (
        (1, 'Très facile'),
        (2, 'Facile'),
        (3, 'Moyen'),
        (4, 'Difficile'),
        (5, 'Très difficile'),
    )
    COST_CHOICES = (
        (1, 'Très bon marché'),
        (2, 'Bon Marché'),
        (3, 'Peu cher'),
        (4, 'Assez cher'),
        (5, 'Très cher'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)
    preparation_time = timedelta.fields.TimedeltaField(null=True, blank=True)
    portion = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, editable=False)
    calory = models.IntegerField(null=True, blank=True)
    sources = models.ManyToManyField(Source, blank=True)
    cost = models.IntegerField(choices=COST_CHOICES,
                               null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES,
                                     null=True, blank=True)
    picture = StdImageField(upload_to='media', null=True, blank=True,
                                  size=(640, 480, True),
                                  thumbnail_size=(200, 200, True))
    hint = models.TextField(blank=True)
    ingredients = models.TextField()
    content = models.TextField()
    category = models.ForeignKey('Category')
    comment = models.TextField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    modification_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ["title"]
        
    def get_difficulty(self):
        difficulty_choices = dict(self.DIFFICULTY_CHOICES)
        if self.difficulty is not None:
            return difficulty_choices[self.difficulty]
        else:
            return ""
            
    def get_cost(self):
        cost_choices = dict(self.COST_CHOICES)
        if self.cost is not None:
            return cost_choices[self.cost]
        else:
            return ""

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def save(self, **kwargs):
        unique_slugify(self, self.title)
        super(Recipe, self).save()
    
class BakingInfo(models.Model):
    FAN_OVEN = 'FO'
    TOP_BOTTOM_HEAT = 'TB'
    TOP_HEAT = 'TH'
    GAS_STOVE = 'GS'
    BAKING_TYPE_CHOICES = (
        (FAN_OVEN, 'Fan Oven'),
        (TOP_BOTTOM_HEAT, 'Top Bottom Heat'),
        (TOP_HEAT, 'Top Heat'),
        (GAS_STOVE, 'Gas Stove'),
    )
    
    TEMP_CELSIUS = 'C'
    TEMP_FAHRENHEIT = 'F'

    TEMPERATURE_UNIT_CHOICES = (
        (TEMP_CELSIUS, '°C'),
        (TEMP_FAHRENHEIT, '°F'),
    )
    
    type = models.CharField(max_length=2,
                            choices=BAKING_TYPE_CHOICES,
                            default=FAN_OVEN)
    temperature = models.IntegerField()
    unit = models.CharField(max_length=1,
                            choices=TEMPERATURE_UNIT_CHOICES,
                            default=TEMP_CELSIUS)
    time = timedelta.fields.TimedeltaField(null=True, blank=True)
    recipe = models.ForeignKey(Recipe)
    
    def __str__(self):
        type_choices = dict(self.BAKING_TYPE_CHOICES)
        unit_choices = dict(self.TEMPERATURE_UNIT_CHOICES)
        return '%s: %s%s (%s)' % (type_choices[self.type], 
                                self.temperature,
                                unit_choices[self.unit],
                                self.time)

    def __unicode__(self):
        type_choices = dict(self.BAKING_TYPE_CHOICES)
        unit_choices = dict(self.TEMPERATURE_UNIT_CHOICES)
        return u'%s: %s%s (%s)' % (type_choices[self.type], 
                                self.temperature,
                                unit_choices[self.unit],
                                self.time)