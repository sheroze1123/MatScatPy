import numpy as np
import sys

def square_well(ab=None, V=None, h=1, order=20):
    """Discretize a problem where the potential is given by a piecewise constant.
    
    Input:
      ab    -- breakpoints between regions where the potential is constant
      V     -- potential values on each interval ab(j) to ab(j+1)
      h     -- maximum element size (default 1)
      order -- maximum element order (default 20)
    """
    
    if ab is None and V is None:
        ab = np.array([-2, -1, 1, 2])
        V  = np.array([0, -10, 0])
    elif V is None:
        V  = np.pad(ab,(1,1),'constant')
        ab = np.array([-2, -1, 1, 2])

    elt = []
    
    for j in range(0,len(V)):
        L = ab[j+1] - ab[j]
        nelt = int(np.ceil(L/h))
        for k in range(1, nelt+1):
            el = {}
            el['a'] = ab[j] + L*(k-1)/nelt 
            el['b'] = ab[j] + L*k/nelt
            el['order'] = order
            el['Vtype'] = 'constant'
            el['V'] = V[j]
            elt.append(el)
    return elt

