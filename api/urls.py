# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

transfer_simp_resource = Resource(Transfer_simpHandler)
transfer_resource = Resource(TransferHandler)
response_resource = Resource(ResponseHandler)

urlpatterns = patterns('',
    url(r'^transfer/(?P<id>\d+)$', transfer_resource),
    url(r'^transfer$', transfer_resource),

    url(r'^transfer_simp/(?P<id>\d+)$', transfer_simp_resource),
    url(r'^transfer_simp', transfer_simp_resource),

    url(r'^response/(?P<id>\d+)$', response_resource),
    url(r'^response', response_resource),

)