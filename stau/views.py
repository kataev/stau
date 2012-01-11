# -*- coding: utf-8 -*-
__author__ = 'bteam'
from variants import variants as vars
from django.utils import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render
from Transfer import Response,TransferPoly

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
        r = Response(v,T=1).linearization().flattening(3).normalization()
#        y = orig.simou()


        return HttpResponse(json.dumps({'data':r.data.tolist()}))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))


def simou(request,var):
    if 'v%s' % var in vars.keys():
        v = vars['v%s' % var]
        r = Response(v,T=1).linearization().flattening(3).normalization()
        tf = r.simou()
        y = tf.step(draw=False)
        print tf


        return HttpResponse(json.dumps({'data':y.tolist(),'tf':{'num':list(tf.num),'den':list(tf.den)}}))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))

