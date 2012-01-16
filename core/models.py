# -*- coding: utf-8 -*-
from django.db import models
from Fields import Base64Field
from Transfer import *

class Response(models.Model,TimeResponse):
    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)
        for f in self._meta.fields:
            if '_base64' in f.name:
                f.dtype = getattr(self,f.db_column+'_dtype','int64')

    data = Base64Field()
    data_dtype = models.CharField(max_length=100)

    time = Base64Field()
    time_dtype = models.CharField(max_length=100)

class Transfer(models.Model):
    def __init__(self, *args, **kwargs):
        super(Transfer, self).__init__(*args, **kwargs)
        for f in self._meta.fields:
            if '_base64' in f.name:
                f.dtype = getattr(self,f.db_column+'_dtype','int64')

    title = models.CharField(max_length=100,default=u'Передаточная функция')
    num = Base64Field()
    num_dtype = models.CharField(max_length=100,default='int64')
    den = Base64Field()
    den_dtype = models.CharField(max_length=100,default='int64')

    step_length = models.PositiveIntegerField(default=300)
    parent = models.ForeignKey('Transfer',null=True)

    @property
    def q(self):
        return TransferPoly(self.num,self.den)

    @property
    def to_json(self):
        return dict(num=self.num.tolist(),den=self.den.tolist())

    def get_absolute_url(self):
        return '/api/transfer/%d' % self.pk


class TransferPoly(TransferPoly):
    @property
    def db(self):
        return Transfer(num=self.num.coeffs,den=self.den.coeffs)


class Transfer_simp(models.Model,TransferSimp):
    def __init__(self, *args, **kwargs):
        super(Transfer_simp, self).__init__(*args, **kwargs)
        for f in self._meta.fields:
            if '_base64' in f.name:
                f.dtype = getattr(self,f.db_column+'_dtype','int64')

    title = models.CharField(max_length=100,default=u'Передаточная функция')
    t = Base64Field()
    t_dtype = models.CharField(max_length=100,default='int64')
    tau = Base64Field()
    tau_dtype = models.CharField(max_length=100,default='int64')

    step_length = models.PositiveIntegerField(default=300)
    parent = models.ForeignKey('Transfer',null=True)


    @property
    def to_json(self):
        return dict(num=self.t.tolist(),den=self.tau.tolist())

    def get_absolute_url(self):
        return '/api/transfer_simp/%d' % self.pk

