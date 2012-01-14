# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from core.models import Transfer,Response,Transfer_simp
from piston.utils import rc

class TransferHandler(BaseHandler):
    model = Transfer
    fields = ('id', 'num','den','title')

    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.data)

        try:
            inst = self.queryset(request).get(pk=attrs.get('pk',0))
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

class ResponseHandler(BaseHandler):
    model = Response
    fields = ('id', 'data','time')

    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.data)

        if not attrs.has_key('time'):
            attrs['time'] = range(len(attrs['data']))

        try:
            inst = self.queryset(request).get(pk=attrs.get('pk',0))
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.normalization()
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

class Transfer_simpHandler(BaseHandler):
    model = Transfer_simp
    fields = ('id', 't','tau','title')

    def create(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.data)

        try:
            inst = self.queryset(request).get(pk=attrs.get('pk',0))
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            inst.save()
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
