# -*- coding: UTF-8 -*-

from django.contrib import admin
from recipes.models import Recipe, Category

class RecipeAdmin(admin.ModelAdmin):
    list_display   = ('title', 'category', 'author', 'date')
    list_filter    = ('author', 'date', 'category')
    date_hierarchy = 'date'
    ordering       = ('date', )
    search_fields  = ('title', 'content', 'ingredients')

    fieldsets = (
        # Fieldset 1 : meta-info (title, author...)
        ('General', {
            'fields': ('title', 'source', 'category',
                        'portion', 'calory')
        }),
        # Fieldset 2 : preparation info
        ('Preparation', {
            'fields': ('preparation_time', 'baking_time', 'baking_temperature')
        }),
        # Fieldset 3 : images
        ('Images', {
            'classes': ['collapse',],
            'fields': ('small_picture', 'big_picture')
        }),
        # Fieldset 2 : content
        ('Content', {
            'fields': ('ingredients', 'content', 'hint', 'comment')
        }),
    )
        
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
