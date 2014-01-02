# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from recipes.views import RecipesListView, \
                          RecipesMonthArchiveView, \
                          RecipeView

urlpatterns = patterns('recipes.views',
    url(r'^$', RecipesListView.as_view(), name='home'),
    
    # Recipe detail by slug
    url(r'^recipe/(?P<slug>[-\w]+)/$',
        RecipeView.as_view(),
        name='recipe_by_slug'),

    # Recipes list by date
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        RecipesMonthArchiveView.as_view(month_format='%m'),
        name='recipes_archive_month'),

    # Recipes list by category slug
    url(r'^category/(?P<category>[-\w]+)/$',
        RecipesListView.as_view(),
        name='recipes_by_category_slug'),
         
    # Recipes by user's name
    url(r'^user/(?P<author>[-\w]+)/$',
        RecipesListView.as_view(),
        name='recipes_by_author'),
        
    # Recipes by difficulty
    url(r'^difficulty/(?P<difficulty>\d+)/$',
        RecipesListView.as_view(),
        name='recipes_by_difficulty'), 
        
    # Recipes by cost
    url(r'^cost/(?P<cost>\d+)/$',
        RecipesListView.as_view(),
        name='recipes_by_cost'),
        
    # Recipes by source
    url(r'^source/(?P<source>[-\w]+)/$',
        RecipesListView.as_view(),
        name='recipes_by_source'),
)