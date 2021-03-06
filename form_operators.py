import numpy as np
from cheb import cheb
from problem_size import problem_size
from eval_potential import eval_potential

def form_operators(elt,is_sparse = 0):
    #add support for when potential is not defined, form_operators_sys
    nelt = len(elt)
    (N, nz) = problem_size(elt)
    K0 = np.zeros((N,N))
    K1 = np.zeros((N,N))
    K2 = np.zeros((N,N))
        
        
    base = 0
    for j in range(0,nelt):
        order      = elt[j]['order']
        (D, x)     = cheb(order)
        lelt       = elt[j]['b'] - elt[j]['a']
        xelt       = elt[j]['a']*(1-x)/2 + elt[j]['b']*(1+x)/2; #scaling from chebyshev grid to (a) and (b)
        K0elt      = -4*np.dot(D,D)/lelt**2 + np.diag(eval_potential(elt[j], xelt))
        K0elt[0,:] = -2*D[0,:]/lelt # derivative on top and bottom
        K0elt[-1,:] =  2*D[-1,:]/lelt
        K0[base:base+len(D),base:base+len(D)] =  K0elt + K0[base:base+len(D),base:base+len(D)]
        K2[base+1:base+order,base+1:base+order] = np.eye(order-1)
        base = base + order
    K1[0,0] = 1
    K1[N-1,N-1] = 1
    return (K0, K1, K2)
