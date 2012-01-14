# -*- coding: utf-8 -*-
__author__ = 'bteam'
from variants import variants as vars
from django.utils import simplejson as json
from django.http import HttpResponse,HttpResponseRedirect
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

def work_response(request,id,mode,flattening=3):
    r = Response.objects.get(pk=id)
    if mode == 'linearization':
        r.linearization()
    if mode == 'normalization':
        r.normalization()
    if mode == 'flattening':
        flattening = int(flattening)
        print type(flattening)
        r.flattening(iter=flattening)
    r.save()
    return HttpResponse(json.dumps({'data':r.data}))

def tangent_and_other(request,id,mode):
    t = Response.objects.get(pk=id)
    if mode == 'tangent':
        t = t.tangent(True)
        ts = Transfer_simp(tau=[t['tau']],t=[t['T']])
        ts.save()
    if mode == 'match3':
        t = t.match3(raw=True)
        ts = Transfer_simp(tau=[t['tau']],t=[t['T']])
        ts.save()
    return HttpResponseRedirect(ts.get_absolute_url())

def simou(request,id,flattening=3):
    t = Response.objects.get(pk=id)
    try:
        r = TimeResponse(np.array(t.data),T=1)
        tf = r.simou()
        print tf
        ts = Transfer(num=tf.num.coeffs,den=tf.den.coeffs)
        ts.save()
        return HttpResponseRedirect(ts.get_absolute_url())
    except ValueError,e:
        y = {'error':True,'message':str(e)}
        return HttpResponse(json.dumps(y))

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

def nyquist(request,id):
    t = Transfer.objects.get(pk=id)
    try:
        a,b,c = t.q.nyquist(plot=False)
        y = dict(a=a.tolist(),b=b.tolist(),c=c.tolist())
    except ValueError,e:
        y = {'error':True,'message':str(e)}
    return HttpResponse(json.dumps(y))

def transfer_simp_step(request,id):
    t = Transfer_simp.objects.get(pk=id)
    l = int(request.GET.get('length',100))+1
    data,time = t.step(l)
    return HttpResponse(json.dumps({'data':data.tolist(),'time':time.tolist()}))

def step(request,id):
    t = Transfer.objects.get(pk=id)
    try:
        s = t.q
        l = int(request.GET.get('length',100))+1
        s.time = np.arange(l)
        time,data = s.step(draw=False,fast=True)
        y = dict(data=data.tolist(),time=time.tolist())
    except ValueError,e:
        y = {'error':True,'message':str(e)}
    return HttpResponse(json.dumps(y))


def simp(request,id,order):
    t = Transfer.objects.get(pk=id)
    tf = t.q.simp(order)
    print t.num,t.den

    ts = Transfer(num=tf.num.coeffs,den=tf.den.coeffs)
    ts.save()
    print t.num,t.den
    print t.q
    print tf
    return HttpResponseRedirect(ts.get_absolute_url())