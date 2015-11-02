import numpy as np
import math 

def cheb(N):
    """
    Compute D = differentiation matrix, x = Chebyshev grid.  
    Adapted from the routine in Trefethen's "Spectral Elements in MATLAB"
    """

    x = np.cos(np.pi * np.arange(0,N+1)/N)
    c = np.ones(N+1)
    c[0]  = 2
    c[N]  = 2
    c = np.multiply(c, np.power( -1, np.arange(0,N+1)))
    c = np.array([c])
    X = np.tile(np.array([x]).T, (1,N+1))
    dX = X - X.T
    D = np.divide( np.dot(c.T, np.divide(1.0,c)), dX + np.eye(N+1))
    D = D - np.diag(np.sum(D,1))
    return (np.fliplr(np.flipud(D)), x[::-1])
