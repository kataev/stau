# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from core.models import Transfer

class TransferHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Transfer
    fields = ('id', 'num', 'den')

#    def create(self, request):
#        print request
#        super(TransferHandler, self).create(request)