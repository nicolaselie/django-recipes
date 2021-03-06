# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.comments.admin import CommentsAdmin

from pagedown.widgets import AdminPagedownWidget
from easy_thumbnails.fields import ThumbnailerImageField
from durationfield.db.models.fields.duration import DurationField

from .models import Recipe, Category, Source, BakingInfo, MarkdownComment
from .widgets import PreviewAdminImageWidget, AdminDurationWidget
from . import get_model

class BakingInfoInline(admin.TabularInline):
    model = BakingInfo
    extra = 0
    fieldsets = ()
    
    formfield_overrides = {
        DurationField: {'widget': AdminDurationWidget(), },
    }

class RecipeForm(forms.ModelForm):
    class Meta:
        widgets = { 'content' : AdminPagedownWidget(), 
                    'ingredients' : AdminPagedownWidget(), }
    
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display   = ('title', 'category', 'author', 
                      'creation_time', 'modification_time')
    list_filter    = ('author', 'creation_time', 'modification_time',
                      'category')
    date_hierarchy = 'modification_time'
    ordering       = ('modification_time', )
    search_fields  = ('title', 'content', 'ingredients')

    fieldsets = (
        # Fieldset 1 : meta-info (title, author...)
        ('General', {
            'fields': ('title', 'sources', 'category', 'difficulty', 'cost',
                        'portion', 'calory', 'picture')
        }),
        # Fieldset 2 : content
        ('Content', {
            'fields': ('ingredients', 'content', 'hint')
        }),
        # Fieldset 3 : preparation info
        ('Preparation', {
            'classes': ['wide',],
            'fields': ('preparation_time', )
        }),
    )
        
    inlines = [BakingInfoInline]
    
    formfield_overrides = {
        ThumbnailerImageField: {'widget': PreviewAdminImageWidget(), },
        DurationField: {'widget': AdminDurationWidget(), },
    }
        
    def save_model(self, request, obj, form, change):
        """ Autofill in author when blank on save models. """
        obj.author = request.user
        obj.save()
        
    def save_formset(self, request, form, formset, change):
        """ Autofill in author when blank on save formsets. """
        instances = formset.save(commit=False)
        for instance in instances:
            instance.author = request.user
            instance.save()
        formset.save_m2m() 
   
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(Source)

if get_model() is MarkdownComment:
    admin.site.register(MarkdownComment, CommentsAdmin)