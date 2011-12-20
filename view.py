#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kataev Denis'
import matplotlib.pyplot as plt
from variants import variants
from stau import *
from inverse_laplase import _riemann
import scipy
from scipy import signal
from scipy import Inf
from scipy.integrate import quad

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
    orig = Response(np.array(variants['v11']),T=1)

    num = np.poly1d([1])
    den = np.poly1d((30, 20, 1))
    system = signal.lti(num,den)
    t,y = system.step(T=np.array(range(0,141)))
    plt.plot(t,y)

    num = np.poly1d([1])
    den = np.poly1d(Response(np.array(t),time=y,T=0.0308513198557).normalization().simou())
    system1 = signal.lti(num,den)
    t1,y1 = system1.step(T=np.array(range(0,141)))
    plt.plot(t1,y1)


#    c = _riemann(lambda x: num(x)/den(x),np.array(range(0,100)),100)
#    plt.plot(range(0,100),c,'-')
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
    system = signal.lti([3.6,1],[130,23, 1])
    t,y = system.step()
    orig = Response(np.array(y),T=10) #Мой вариант 14
    orig.linearization().flattening(1).normalization()
    s = orig.simou()
#    system1 = signal.lti([50,1],[9.37850627e+06,   3.43973516e+04,   1.18723200e+04, 2.28335083e+02,   1.00000000e+00])
#    t1,y1 = system.step()
#    plt.plot(orig.time,orig.data,'-',label=u'Оригинал') #original
#    plt.plot(orig.time,[p(x) for x in orig.time],'-',label=u'1-h') #invert
    plt.plot(t,y,'-',label=u'simou') #original
#    plt.plot(t1,y1,'x',label=u'simou1') #original
#    plt.ylim([0,1])
#    plt.xlim([0,orig.time.max()])
    plt.legend(loc='upper left')
#    plt.show()

def show_simou_obs_error():
    """ Тестирование передаточной функции """
    system = signal.lti([3.6,1],[130,23, 1])
    t,y = system.step()

    orig = Response(np.array(y),T=1) #Мой вариант 14
    orig.linearization().flattening(5).normalization()
    orig.data = 1 - orig.data
    plt.plot(orig.time,orig.data,'-',label=u'Оригинал') #original
    plt.plot(orig.time,orig.data*pow(orig.time,1),'-',label=u'1 площядь') #original
#    plt.plot(orig.time,orig.data*pow(orig.time,2),'-',label=u'2 площядь') #original
#    plt.plot(orig.time,orig.data*pow(orig.time,3),'-',label=u'3 площядь') #original
#    plt.ylim([0,1])
    plt.xlim([0,orig.time.max()])
    plt.legend(loc='upper left')
    plt.show()

def test_poly_n():
    """ Тест полиномной передаточной функции и системы lti """
    num = np.poly1d([1])
    den = np.poly1d([130,23,1])

    orig = Response(np.array(variants['v14']),T=10)

    system = signal.lti(num,den)
    t,y = system.step(T=orig.time)

    y1 = _riemann(lambda x: num(x)/den(x)/x,orig.time,300)

    plt.plot(t,y,label='system')
    plt.plot(t,y1)
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
#    test_contact4()
    test_transfer()
#    show_simou_obs_error()
#    test_lf()
#    test_poly_n()
#    all_vars()
