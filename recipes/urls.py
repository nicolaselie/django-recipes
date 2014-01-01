# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from recipes.views import RecipesListView, \
                          RecipesCategoryView, \
                          RecipesMonthArchiveView, \
                          RecipeView

urlpatterns = patterns('recipes.views',
    url(r'^$', RecipesListView.as_view(), name='home'),
    
    # Recipe detail by pk
    url(r'^recpe/(?P<pk>\d+)/$',
        RecipeView.as_view(),
        name='recipe_by_pk'),
    # Recipe detail by slug
    url(r'^recipe/(?P<slug>[-\w]+)/$',
        RecipeView.as_view(),
        name='recipe_by_slug'),

    # Recipes list by date    
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        RecipesMonthArchiveView.as_view(month_format='%m'),
        name='recipe_archive_month'),

    # Recipes list by category ID
    url(r'^category/(?P<pk>\d+)/$',
        RecipesCategoryView.as_view(),
        name='list_recipes_by_category_id'),
    
    # Recipes list by category slug
    url(r'^category/(?P<slug>[-\w]+)/$',
        RecipesCategoryView.as_view(),
        name='list_recipes_by_category_slug'),
)