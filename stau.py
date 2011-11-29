# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as inter
from scipy.misc import derivative
from variants import variants
from scipy import signal
import string

class Response:
    def __init__(self,data,time=None,T=None):
        """
        Инициализация класса
        """
        self.data = data.copy()
        if not T:
            raise u'Нету временной постоянной ни массива данных'
        self.t = T
        self.make_time()

    def make_time(self,T=None):
        """
        Берёт или создает массив по шагу времени
        """
        if not T: T = self.t
        self.time = np.arange(0,len(self.data)*T,T)
        return self

    def linearization(self):
        """
        Лианеризация повторяющихся значений из-за низкой разрешаюшей способности
        """
        z = self.data.copy()
        w = []
        for idx,val in enumerate(z):
            w.append(idx)
            if z[w[0]]!=val:
                z.put(w,np.linspace(z[w[0]],z[w[-1]],len(w)))
                w=[]
        self.data = z
        return self

    def normalization(self):
        """
        Нормализация к [0:1]
        """
        z = self.data.copy()
        min = z.min()
        max = z.max()
        for i,val in enumerate(z):
            z[i] = (val-min)/(max-min)
        self.data = z
        return self

    def remove_delay(self):
        """
        Обрезает стагнацию характеристики в начале и конце
        """
        data = self.data.copy()
        time = self.time.copy()
        q,e = 0,0
        for i,val in enumerate(data):
            if data[0]+1 > val: q=i
#        for i,val in enumerate(data):
#            if data[-1] == val:
#                e=i
#                break
        self.data = data[q:]#e+1]
        self.time = time[q:]#e+1]
        self.make_time()
        return self

    def flattening(self,iter=1):
        """
        Сглажевание методом 3 точек
        """
        data = self.data.copy()
        if iter <=0: raise u'1 или более раз'
        for a in range(iter):
            data[0], data[1] = (5*data[0] + 2*data[1] - data[2])/6, (data[0] + data[1] + data[2])/3
            for i in range(3,len(data)-1):
                data[i] = (data[i-2] + data[i-1] + data[i+1])/3
            data[-1] = (-data[-4] + 2*data[-3] + 5*data[-2])/6
            self.data = data
        return self

    def tangent(self):
        """
        Метод касательной.
        """
        data = self.data.copy()
        D = self.t
        z = np.array([a-b for a,b in zip(data[1:],data)])
        j = np.where(z==z.max())[0][0]
        A = self.time[j-1]+D/2
        B = (data[j]+data[j+1])/2
        T = D/(data[j+1] - data[j])
        m = np.where(data==data.max())
        tau = self.time[j-1]-data[j]*T

        return {'point':(A,B,j),'T':T,'tau':tau}

    def tangent_poly(self):
        """
        Метод касательной
        Методом полинома, определяем точку где 2 производная ровна нулю.
        """
        poly = np.poly1d(np.polyfit(self.time,self.data,3))
        point = np.poly1d(poly.deriv(m=2)).r[0]
        der1 = np.poly1d(poly.deriv(m=1))
        tang = np.poly1d([der1(point),poly(point)-point*der1(point)])
        tau = tang.r[0]
        T = (1-tang[0])/tang[1]-tau
        j = int(point/self.t)
        return {'point':(point,tang(point),j),'T':T,'tau':tau}

    def match3(self,tangent):
        T = tangent['T']*(1-tangent['point'][1])
        tau = tangent['point'][0]-T*np.log(tangent['T']/T)
        return {'T':T,'tau':tau}

class Transfer:
    def __init__(self,T,tau):
        self.tau = tau
        self.T = T

    def __str__(self):
        num = np.poly1d([1],variable='s')
        den = np.poly1d([self.T,1],variable='s')
        l = max(len(str(num).strip()),len(str(den).strip()))
        n = unicode(num).split('\n')
        n[1]=n[1].center(l)
        n[1]+=u' -%f S\n'% self.tau + u'-'*l + u' e'
        return n[0]+u'\n'+n[1]+u'\n'+str(den)



def all_vars():
    """ Работа со всеми вариантами одновременно """
    q = []
    for v in variants:
#        q.append(Response(np.array(variants[v]),T=10).remove_delay().linearization().flattening().normalization())
        q.append(Response(np.array(variants[v]),T=10).flattening().normalization())
    w=[]
    for a in q:
        w.append(a.time)
        w.append(a.data)
        w.append('-')
    plt.plot(*w)
    plt.show()

def test():
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

def test_lf():
    """
    Проба scipy системы.
    """
    num = np.poly1d([3.6,1])
    den = np.poly1d([130,23,1])
    system = signal.lti(*signal.tf2ss(num,den))
    d = system.step()
    plt.plot(d[0],d[1],'-',)
    plt.show()

def test_transfer():
    p = Response(np.array(variants['v13']),T=10)
    p.linearization().flattening(3).normalization()

    poly =  p.tangent_poly()
    t = Transfer(poly['T'],poly['tau'])
    print t

if __name__ == '__main__':
    test()
#    all_vars()