# -*- coding: UTF-8 -*-

from django.contrib import admin
from recipes.models import Recipe, Category, Source, BakingInfo

class BakingInfoInline(admin.TabularInline):
    model = BakingInfo
    extra = 0
    fieldsets = ()

class RecipeAdmin(admin.ModelAdmin):
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
            'fields': ('title', 'sources', 'category',
                        'portion', 'calory')
        }),
        # Fieldset 2 : images
        ('Images', {
            'classes': ['collapse',],
            'fields': ('small_picture', 'big_picture')
        }),
        # Fieldset 3 : content
        ('Content', {
            'fields': ('ingredients', 'content', 'hint', 'comment')
        }),
        # Fieldset 4 : preparation info
        ('Preparation', {
            'classes': ['wide',],
            'fields': ('preparation_time', )
        }),
    )
        
    inlines = [BakingInfoInline]
        
    def save_model(self, request, obj, form, change):
        """ Autofill in author when blank on save models. """
        print obj.rating
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