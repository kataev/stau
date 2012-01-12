# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'stau.views.home', name='home'),
#    url(r'^stau/', include('stau.foo.urls')),
    (r'^var/(?P<var>\d+)$', 'views.variants'),
    (r'^var/(?P<var>\d+)/clear$', 'views.do_all'),
    (r'^var/(?P<var>\d+)/simou/$', 'views.simou'),
    (r'^var/(?P<var>\d+)/simou/(?P<order>\d+)/$', 'views.simou'),
    (r'^transfer/(?P<num>.+)/(?P<den>.+)/$', 'views.transfer'),
    (r'^transfer/(?P<id>\d+)$', 'views.get_transfer'),
    (r'^transfer/(?P<id>\d+)/step$', 'views.step'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
