#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Kataev Denis'
import numpy as np
from inverse_laplase import _riemann
from scipy import factorial as fac
from scipy.integrate import quad
from scipy import signal
from control import matlab
from matplotlib import pyplot as plt

class Response:
    def __init__(self,data,time=None,T=None):
        """ Класс динамической характеристики """
        self.data = data.copy()
        self.t = T
        if time is not None:
            self.time=time
        else:
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

    def tangent(self,raw=False):
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
        if raw:
            return {'point':(A,B,j),'T':T,'tau':tau}
        else:
            return Transfer(T,tau)

    def tangent_poly(self,raw=False):
        """ Метод касательной
        Методом полинома, определяем точку где 2 производная ровна нулю. """
        poly = np.poly1d(np.polyfit(self.time,self.data,3))
        point = np.poly1d(poly.deriv(m=2)).r[0]
        der1 = np.poly1d(poly.deriv(m=1))
        tang = np.poly1d([der1(point),poly(point)-point*der1(point)])
        tau = tang.r[0]
        T = (1-tang[0])/tang[1]-tau
        j = int(point/self.t)
        if raw:
            return {'point':(point,tang(point),j),'T':T,'tau':tau}
        else:
            return Transfer(T,tau)

    def match3(self,tangent=None,raw=False):
        if not tangent: tangent=self.tangent(raw=True)
        T = tangent['T']*(1-tangent['point'][1])
        tau = tangent['point'][0]-T*np.log(tangent['T']/T)
        if raw:
            return {'T':T,'tau':tau,'point':tangent['point']}
        else:
            return Transfer(T,tau)

    def contact4(self,match3=None,raw=False):
        if not match3: match3=self.match3(raw=True)
        j = match3['point'][2]-1
        a = self.time[j],self.data[j]
        i = np.where(self.data>=0.75)[0][0]
        b = self.time[i],self.data[i]
#        print a,b
        if a and b:
            tau = (b[0]*np.log(1-b[1]) - a[0]*np.log(1-b[1]))/(np.log(1-a[1]) - np.log(1-b[1]))
            T = tau/np.log(1-a[1])
        if tau and T:
            if raw:
                return {'T':T,'tau':-1*tau,'point':match3['point']}
            else:
                return Transfer(T,tau)

    def orman(self,raw=False):
        i = np.where(self.data>=0.33)[0][0]
        a = self.time[i],self.data[i]

        j = np.where(self.data>=0.7)[0][0]
        b = self.time[j],self.data[j]

        T = 1.25*(b[0]-a[0])
        tau = (3*a[0]-b[0])/2

        if raw:
            return {'T':T,'tau':tau}
        else:
            return Transfer(T,tau)

    def simou(self):
        end = self.time[-1]
        fi = np.poly1d(np.polyfit(self.time,1-self.data,4))
        nu = np.empty(10)
        nu.fill(0)
        nu[0] = quad(lambda t: fi(t),0,end)[0]
        nu[1] = quad(lambda t: pow(-t,1)*fi(t),0,end)[0]
        nu[2] = quad(lambda t: pow(-t,2)*fi(t),0,end)[0]/2
        s = np.empty(10)
        s.fill(0)
        s[1] = nu[0]
        s[2] = nu[0]*s[1]+nu[1]
        for k in range(3,10):
            s[k] = (nu[:k-1]*s[1:k][::-1]).sum()+nu[k-1]
            nu[k] = quad(lambda t: pow(-t,k)*fi(t),0,end)[0]/fac(k)
            if s[k] < s[k-1]: break
        last = max(s.nonzero()[0])

        b = np.empty(10)
        b.fill(0)
        a = np.empty(10)
        a.fill(0)
        b[0]=1
        if s[last] < 0 : b[1] = -s[last]/s[last-1]

        a[0]= 1
        for k in range(1,last):
            a[k]=b[k] + s[k]+(b[1:k]*s[1:k][::-1]).sum()
        print s
        return TransferPoly(b[::-1],a[::-1],self.time)

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
        return _riemann(lambda s:np.exp(-s*self.tau)/(self.T*s+1)/s,time,100)

class TransferPoly:
    def __init__(self,num,den,time=np.arange(100)):
        self.time = time
        self.num = np.poly1d(num,variable='s')
        self.den = np.poly1d(den,variable='s')
        ss = signal.tf2ss(self.num,self.den)
        self.ss = matlab.ss(*ss)

    def __call__(self, s):
        return self.num(s)/self.den(s)

    def __str__(self):
        num = str(self.num)
        den = str(self.den)
        return num+'\n'+'-'*len(num)+'\n'+den

    def afchx(self):
        return matlab.bode(self.ss)

    def nykwist(self):
        return matlab.nyquist(self.ss)

    def step(self):
        """ Во временную область """
        y = _riemann(lambda s: self(s)/s,self.time,100)
        plt.plot(self.time,y,label=u'ПФ скачок')
        plt.grid()
        return y