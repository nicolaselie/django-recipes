# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments import Comment

import datetime

import timedelta
from easy_thumbnails.fields import ThumbnailerImageField
from durationfield.db.models.fields.duration import DurationField
from ratings.models import Ratings, RatedItemBase

from markdown import markdown

from slugify import unique_slugify
    
class Rating(RatedItemBase):
    content_object = models.ForeignKey('Recipe')

class Source(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)
    url = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
        
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
    preparation_time = DurationField(null=True, blank=True)
    portion = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, editable=False)
    calory = models.IntegerField(null=True, blank=True)
    sources = models.ManyToManyField(Source, blank=True)
    cost = models.IntegerField(choices=COST_CHOICES,
                               null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES,
                                     null=True, blank=True)
    picture = ThumbnailerImageField(upload_to='media', blank=True)
    hint = models.TextField(blank=True)
    ingredients = models.TextField()
    ingredients_markup = models.TextField(editable=False)
    content = models.TextField()
    content_markup = models.TextField(editable=False)
    category = models.ForeignKey('Category')
    ratings = Ratings(Rating)
    creation_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    modification_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        
        # Markdown part from http://www.yaconiello.com/blog/part-1-creating-blog-system-using-django-markdown
        self.content_markup = markdown(self.content)
        self.ingredients_markup = markdown(self.ingredients)
        
        super(Recipe, self).save(*args, **kwargs)
    
class BakingInfo(models.Model):
    FAN_OVEN = 'F'
    TOP_BOTTOM_HEAT = 'H'
    TOP_HEAT = 'T'
    BOTTOM_HEAT = 'B'
    GAS_STOVE = 'G'
    PAN = 'P'
    BAKING_TYPE_CHOICES = (
        (FAN_OVEN, u'Fan Oven'),
        (TOP_BOTTOM_HEAT, u'Top Bottom Heat'),
        (TOP_HEAT, u'Top Heat'),
        (BOTTOM_HEAT, u'Bottom Heat'),
        (GAS_STOVE, u'Gas Stove'),
        (PAN, u'Pan'),
    )
    
    TEMP_CELSIUS = 'C'
    TEMP_FAHRENHEIT = 'F'
    TEMP_THERMOSTAT = 'T'

    TEMPERATURE_UNIT_CHOICES = (
        (TEMP_CELSIUS, u'°C'),
        (TEMP_FAHRENHEIT, u'°F'),
        (TEMP_THERMOSTAT, u'Thermostat'),
    )
    
    type = models.CharField(max_length=2,
                            choices=BAKING_TYPE_CHOICES,
                            default=FAN_OVEN)
    temperature = models.IntegerField()
    unit = models.CharField(max_length=1,
                            choices=TEMPERATURE_UNIT_CHOICES,
                            default=TEMP_CELSIUS)
    time = DurationField(null=True, blank=True)
    recipe = models.ForeignKey(Recipe)
    
    def get_display(self, *args, **kwargs):
        if self.unit == self.TEMP_THERMOSTAT:
            return self.get_unit_display() + " " + str(self.temperature)
        else:
            return str(self.temperature) + self.get_unit_display()
    
    def __str__(self):
        return '%s: %s (%s)' % (self.get_type_display(),
                                self.get_display(),
                                self.time)

    def __unicode__(self):
        return '%s: %s (%s)' % (self.get_type_display(),
                                self.get_display(),
                                self.time)
    
class MarkdownComment(Comment):
    comment_markup = models.TextField(editable=False)
        
    def save(self, *args, **kwargs):
        # Markdown part from http://www.yaconiello.com/blog/part-1-creating-blog-system-using-django-markdown
        self.comment_markup = markdown(self.comment)
        super(MarkdownComment, self).save(*args, **kwargs)