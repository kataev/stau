# -*- coding: utf-8 -*-
from django.db import models
from Fields import Base64Field
from Transfer import TransferPoly,TimeResponse

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

    @property
    def q(self):
        return TransferPoly(self.num,self.den)

    @property
    def to_json(self):
        return dict(num=self.num.tolist(),den=self.den.tolist())


class TransferPoly(TransferPoly):
    @property
    def db(self):
        return Transfer(num=self.num.coeffs,den=self.den.coeffs)