#Compute D = differentiation matrix, x = Chebyshev grid.  Adapted
# from the routine in Trefethen's "Spectral Elements in MATLAB"

import numpy as np
import math 
def cheb(N):
    j = np.linspace(0,N,N+1)
    pi = math.pi
    x = np.cos(j*pi/N)
    c = np.zeros(N+1)
    c[0]  = 2
    c[N]  = 2
    c[1:N] = np.ones(N-1)
    D = np.zeros((N+1,N+1))
    #off diagonal entries
    for p in range(0,N+1):
        for q in range(0,N+1):
            if(p!=q):
                D[p,q] = (c[p]/c[q])*((-1)**(p+q))/(x[p]-x[q])
    #diagonal entries by summing columns
    for p in range(0,N+1):
        D[p,p] = -1*np.sum(D[p,:])
        
    return {'D':D, 'x':x}
                
