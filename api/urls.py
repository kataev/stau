# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import TransferHandler

transfer_resource = Resource(TransferHandler)

urlpatterns = patterns('',
    url(r'^transfer/(?P<id>\d+)$', transfer_resource),
    url(r'^transfer$', transfer_resource),

)