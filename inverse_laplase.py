import numpy

def factorial(n):
    if n == 0:
        return 1
    elif n < 0:
        print 'cannot take the factorial of a negative number'
        return
    else:
        #algorithm from internet posting by Lawrence David
        return reduce(lambda i, j: i*j, xrange(1, n+1))

def _riemann(transform, timearray, N, show_progress=False):
    '''This algorithm is proposed by Tzou, Oezisik and Chiffelle (1994)'''
    
    #do some checking on the time array
    if numpy.any(timearray<0):
            raise ValueError('Cannot evaluate for negative time')

    if timearray[0] == 0:
        timearray = numpy.array(timearray, numpy.float64)
        timearray[0] = 0.00001

    b = 4.7
    f = numpy.array([])
    
    for t in timearray:
        rsum = .0
        for n in range(1, N+1): rsum += transform(b/t + 1J*n*numpy.pi/t)*((-1)**n).real
#        rsum = reduce(lambda s,n: s+transform(b/t + 1J*n*numpy.pi/t)*((-1)**n).real,xrange(N))
        tempval2 = transform(b/t)*0.5
        fval = numpy.exp(b)/t * (tempval2 + rsum)
        f = numpy.append(f,fval)
    return f
