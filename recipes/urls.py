# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from recipes.views import ListRecipes

urlpatterns = patterns('recipes.views',
    url(r'^$', ListRecipes.as_view(), name='home'),
    url(r'^recipe/(?P<id>\d+)/$', 'view_recipe'),
    url(r'^recipes/(?P<year>\d{4})/(?P<month>\d{2})/$', 'list_recipes_by_date'),
    url(r'^category/(?P<id>\d+)/$', 'list_recipes_by_category'),
)