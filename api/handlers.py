# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from core.models import Transfer

class TransferHandler(BaseHandler):
    allowed_methods = ('GET','POST','PUT')
    model = Transfer
    fields = ('id', 'num','den')

#    def read(self, request, id=None):
#        if id:
#            t = Transfer.objects.get(pk=id)
#            return t
#        else:
#            return Transfer.objects.all()
