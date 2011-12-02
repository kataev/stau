#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kataev Denis'
import matplotlib.pyplot as plt
from variants import variants
from stau import *
from inverse_laplase import _riemann
from scipy import signal

def all_vars():
    """ Работа со всеми вариантами одновременно """
    q = []
    for v in variants:
        q.append(Response(np.array(variants[v]),T=10).flattening().normalization())
    w=[]
    for a in q:
        w.append(a.time)
        w.append(a.data)
        w.append('-')
    plt.plot(*w)
    plt.show()

def test():
    """ Тестирование методов у класса Response """
    p = Response(np.array(variants['v13']),T=10)
    p.linearization().flattening(3).normalization()

    match3 = p.match3(tangent)
    tangent =  p.tangent()

    poly =  p.tangent_poly()
    match3_poly = p.match3(poly)

    print u'Касательная'
    print tangent
    print match3

    print u'Касательная через полином'
    print poly
    print match3_poly
#    plt.plot(p.time,p.data,'-',)
#    plt.plot(poly['tau'],0,'o',tangent['tau'],0,'x')
#    plt.plot(poly['T']+poly['tau'],1,'o',tangent['T']+tangent['tau'],1,'x')
#    plt.plot(match3['T']+match3['tau'],1,'o',match3['T']+match3['tau'],1,'x')
#    plt.plot(poly['point'][0],poly['point'][1],'o',tangent['point'][0],tangent['point'][1],'x')
#    plt.show()
    pass

def test_lf():
    """ Проба scipy системы. """
    num = np.poly1d([3.6,1])
    den = np.poly1d([130,23,1])
    system = signal.lti(*signal.tf2ss(num,den))
    d = system.step()
    plt.plot(d[0],d[1],'-',)
    plt.show()

def test_contact4():
    orig = Response(np.array(variants['v11']),T=10) #Мой вариант 14
    orig.linearization().flattening(3).normalization()

    plt.plot(orig.time,orig.data,'-',label=u'Оригинал') #original
    plt.plot(orig.time,Transfer(**orig.contact4()).to_time(orig.time).data,'-',label=u'Соприкосновения 4')
    plt.plot(orig.time,Transfer(**orig.orman()).to_time(orig.time).data,'-',label=u'Орман')
    plt.legend(loc='upper left')
    plt.show()

def test_transfer():
    """ Тестирование передаточной функции """
    orig = Response(np.array(variants['v14']),T=10) #Мой вариант 14
    orig.linearization().flattening(1).normalization()

    plt.plot(orig.time,orig.data,'-',label=u'Оригинал') #original
    plt.plot(orig.time,Transfer(**orig.tangent()).to_time(orig.time).data,'-',label=u'Касательная')
    plt.plot(orig.time,Transfer(**orig.match3(orig.tangent())).to_time(orig.time).data,'-',label=u'3 точки')
    plt.plot(orig.time,Transfer(**orig.contact4()).to_time(orig.time).data,'-',label=u'Соприкосновения 4')
    plt.plot(orig.time,Transfer(**orig.orman()).to_time(orig.time).data,'-',label=u'Орман')
    plt.ylim([0,1])
    plt.xlim([0,orig.time.max()])
    plt.legend(loc='upper left')
    plt.show()

def test_poly_n():
    """ Тест полиномной передаточной функции и системы lti """
    num = [20,1]
    den = [130,23,1]

    system = signal.lti(num,den)
    t,i = system.step()

    plt.plot(t,i)
    plt.show()

if __name__ == '__main__':
#    test_contact4()
#    test_transfer()
    test_poly_n()
#    all_vars()