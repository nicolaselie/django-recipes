# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recipes.views.home', name='home'),
    url(r'^', include('recipes.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ratings/', include('ratings.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
