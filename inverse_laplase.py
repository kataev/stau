#!/usr/bin/env python
import numpy
__author__ = 'S. Chris Colbert' # sccolbert@gmail.com http://mail.scipy.org/pipermail/scipy-user/2009-November/023478.html

def _riemann(transform, timearray, N, show_progress=False):
    '''This algorithm is proposed by Tzou, Oezisik and Chiffelle (1994)'''
    
    if numpy.any(timearray<0):
            raise ValueError('Cannot evaluate for negative time')

    if timearray[0] == 0:
        timearray = numpy.array(timearray, numpy.float64)
        timearray[0] = 0.00001

    b = 4.7

    f=map(lambda t:numpy.exp(b)/t * (transform(b/t)/2 + reduce(lambda s,n: s+(transform(b/t + 1J*n*numpy.pi/t)*((-1)**n)).real,xrange(0,N))),timearray)
    return numpy.array(f)


if __name__=='__main__':
    print '1/s'
    print _riemann(lambda s:1/s**1,xrange(1,10),100)
    print '1/s^2'
    print _riemann(lambda s:1/s**2,xrange(1,10),100)