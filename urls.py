# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stau.views.home', name='home'),

    url(r'^variant/(?P<var>\d+)$', 'views.variants'),

    url(r'^api/transfer/(?P<id>\d+)/step$', 'views.step'),
    url(r'^api/transfer/(?P<id>\d+)/nyquist', 'views.nyquist'),
    url(r'^api/transfer/(?P<id>\d+)/simp/(?P<order>\d+)', 'views.simp'),

    url(r'^api/transfer_simp/(?P<id>\d+)/step$', 'views.transfer_simp_step'),

    url(r'^api/response/(?P<id>\d+)/simou', 'views.simou'),
    url(r'^api/response/(?P<id>\d+)/(?P<mode>normalization|linearization)', 'views.work_response'),
    url(r'^api/response/(?P<id>\d+)/(?P<mode>flattening)/(?P<flattening>\d+)', 'views.work_response'),
    url(r'^api/response/(?P<id>\d+)/(?P<mode>tangent|match3)', 'views.tangent_and_other'),

    (r'^api/', include('api.urls'))
)
