#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kataev Denis'
import numpy as np
from scipy import signal
from inverse_laplase import _riemann

class Response:
    def __init__(self,data,time=None,T=None):
        """ Инициализация класса """
        self.data = data.copy()
        if not T:
            raise u'Нету временной постоянной ни массива данных'
        self.t = T
        self.make_time()

    def make_time(self,T=None):
        """ Берёт или создает массив по шагу времени """
        if not T: T = self.t
        self.time = np.arange(0,len(self.data)*T,T)
        return self

    def linearization(self):
        """ Лианеризация повторяющихся значений из-за низкой разрешаюшей способности """
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
        """ Нормализация к [0:1] """
        z = self.data.copy()
        min = z.min()
        max = z.max()
        for i,val in enumerate(z):
            z[i] = (val-min)/(max-min)
        self.data = z
        return self

    def remove_delay(self):
        """ Обрезает стагнацию характеристики в начале и конце """
        data = self.data.copy()
        time = self.time.copy()
        q,e = 0,0
        for i,val in enumerate(data):
            if data[0]+1 > val: q=i
        self.data = data[q:]
        self.time = time[q:]
        self.make_time()
        return self

    def flattening(self,iter=1):
        """ Сглажевание методом 3 точек """
        data = self.data.copy()
        if iter <=0: return self
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
        """ Метод касательной
        Методом полинома, определяем точку где 2 производная ровна нулю. """
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
    def __init__(self,T,tau,point=None):
        self.tau = tau
        self.T = T

    def __str__(self):
        """ Вывод в читаемом виде """
        num = np.poly1d([1],variable='s')
        den = np.poly1d([self.T,1],variable='s')
        l = max(len(str(num).strip()),len(str(den).strip()))
        n = unicode(num).split('\n')
        n[1]=n[1].center(l)
        n[1]+=u' -%f s\n'% self.tau + u'-'*l + u' e'
        return n[0]+u'\n'+n[1]+u'\n'+str(den)

    def to_time(self,time):
        """ Во временную область """
        self.data = _riemann(lambda s:np.exp(-s*self.tau)/(self.T*s+1)/s,time,100)
        return self
