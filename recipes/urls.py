# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from recipes.views import ListRecipes, ListRecipesByDate, \
                          ListRecipesByCategory, RecipeView

urlpatterns = patterns('recipes.views',
    url(r'^$', ListRecipes.as_view(), name='home'),
    
    # Recipe detail by pk
    url(r'^recipes/(?P<pk>\d+)/$',
        RecipeView.as_view(),
        name='recipe_by_pk'),
    # Recipe detail by slug
    url(r'^recipes/(?P<slug>[-\w]+)/$',
        RecipeView.as_view(),
        name='recipe_by_slug'),
    
    # Recipes list by date
    url(r'^recipes/(?P<year>\d{4})/(?P<month>\d{2})/$',
        ListRecipesByDate.as_view(),
        name='list_recipes_by_date'),
    # Recipes list by category
    url(r'^category/(?P<pk>\d+)/$',
        ListRecipesByCategory.as_view(),
        name='list_recipes_by_category'),
)