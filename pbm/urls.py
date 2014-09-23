"""
    pbm.urls

"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as pbm_views

urlpatterns = patterns('',
    url(r'^$', pbm_views.index, name='pbm-index'),
)
