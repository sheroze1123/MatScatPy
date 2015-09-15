import numpy as np
import sys

class Element:
    def __init__(self, a, b, order, Vtype, V):
        self.a     = a
        self.b     = b
        self.order = order
        self.Vtype = Vtype
        self.V     = V

def square_well(ab=np.array([-2, -1, 1, 2]), V=np.array([0, -10, 0]), h=1, order=20):
    """Discretize a problem where the potential is given by a piecewise constant.
    
    Keyword arguments:
      ab    -- breakpoints between regions where the potential is constant
      V     -- potential values on each interval ab(j) to ab(j+1)
      h     -- maximum element size (default 1)
      order -- maximum element order (default 20)
    """
    
    if len(sys.argv) == 2:
        V  = np.pad(ab,(1,1),'constant')
        ab = np.array([-2, -1, 1, 2])

    elt = []
    
    for j in range(0,len(V)):
        L = ab[j+1] - ab[j]
        nelt = int(np.ceil(L/h))
        for k in range(1, nelt+1):
            a = ab[j] + L*(k-1)/nelt 
            b = ab[j] + L*k/nelt
            el = Element(a, b, order, 'constant', V[j])            
            elt.append(el)

    return elt

