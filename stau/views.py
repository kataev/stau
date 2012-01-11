# -*- coding: utf-8 -*-
__author__ = 'bteam'
from variants import variants as vars
from django.utils import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,'index.html',{'vars':vars.keys()})

def variants(request,var):
    if 'v%s' % var in vars.keys():
        return HttpResponse(json.dumps(vars['v%s' % var]))
    else:
        return HttpResponse(json.dumps({'errors':u'Нет такого варианта'}))


