# -*- coding: utf-8 -*-
from django.db import models
from Fields import Base64Field

class Response(models.Model):
    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)
        for f in self._meta.fields:
            if '_base64' in f.name:
                f.dtype = getattr(self,f.db_column+'_dtype','int64')

    data  = Base64Field()
    data_dtype = models.CharField(max_length=100)

class Transfer(models.Model):
    def __init__(self, *args, **kwargs):
        super(Transfer, self).__init__(*args, **kwargs)
        for f in self._meta.fields:
            if '_base64' in f.name:
                f.dtype = getattr(self,f.db_column+'_dtype','int64')

    num = Base64Field()
    den = Base64Field()