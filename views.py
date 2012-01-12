# -*- coding: utf-8 -*-
__author__ = 'bteam'
from variants import variants as vars
from django.utils import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render
from core.models import *
import numpy as np

def home(request):
    k = map(lambda q: int(q.split('v')[1]),vars.keys())
    k = sorted(k)
    return render(request,'index.html',{'vars':k})

def variants(request,var):
    if 'v%s' % var in vars.keys():
        return HttpResponse(json.dumps({'data':vars['v%s' % var]}))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))


def do_all(request,var):
    if 'v%s' % var in vars.keys():
        v = vars['v%s' % var]
        r = TimeResponse(v,T=1).linearization().flattening(3).normalization()
        return HttpResponse(json.dumps({'data':r.data.tolist()}))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))

def simou(request,var,order=0):
    if 'v%s' % var in vars.keys():
        v = vars['v%s' % var]
        r = TimeResponse(v,T=1).linearization().flattening(3).normalization()
        tf = r.simou()
        order = int(order)
        if order and order < tf.order:
            tf = tf.simp(order)
        y = tf.step(draw=False,fast=True)

        print tf

        return HttpResponse(json.dumps({'data':y.tolist(),'tf':{'num':tf.num.coeffs.tolist(),'den':tf.den.coeffs.tolist()}}))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))


def transfer(request,num,den):
    dtype = request.GET.get('dtype','int64')
    try:
        num = np.fromstring(num,dtype=dtype,sep=',')
        den = np.fromstring(den,dtype=dtype,sep=',')
    except TypeError,e:
        return HttpResponse(json.dumps({'error':True,'message':str(e)}))
    t = TransferPoly(num,den)
    tf = t.db
    tf.save()
    return HttpResponse(json.dumps({'tf':{'id':tf.id,'num':num.tolist(),'den':den.tolist()}}))


def get_transfer(request,id):
    t = Transfer.objects.get(pk=id)
    print t.q
    return HttpResponse(json.dumps(t.to_json))


def step(request,id):
    t = Transfer.objects.get(pk=id)
    y =  t.q.step(draw=False,fast=True).tolist()
    return HttpResponse(json.dumps(y))