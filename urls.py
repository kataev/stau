# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^api/', include('api.urls')),
    url(r'^$', 'stau.views.home', name='home'),
    url(r'^api/transfer/(?P<id>\d+)/step$', 'views.step'),
    url(r'^api/transfer/(?P<id>\d+)/simp/(?P<order>\d+)', 'views.simp'),
        (r'^transfer/(?P<num>.+)/(?P<den>.+)/$', 'views.transfer'),
)
