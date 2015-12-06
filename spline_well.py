from clampedspline import *
import numpy as np
def spline_well(xx=None, Vx=None, h=1, order=20):
    """elt = spline_well(xx, Vx, h, order)
    %
    % Discretize a problem where the potential is given by a spline.
    % Input:
    %   xx    - interpolation points
    %   Vx    - spline values at the points
    %   h     - maximum element size (default: 1)
    %   order - maximum element order (default: 20)"""
    if xx is None and Vx is None:
        Vx = [0,0.5,1,0.5, 0]
        xx = [-1,-0.5,0,0.5,1]

    elt = []
    pp = cubic_spline_get_coeffs(xx, Vx, clamped = True)
    L = xx[-1] - xx[0]
    nelt = int(np.ceil(L/h))
    for k in range(1, nelt+1):
        el = {}
        el['a'] = xx[0] + L*(k-1)/nelt 
        el['b'] = xx[0] + L*k/nelt
        el['order'] = order
        el['Vtype'] = 'spline'
        el['V'] = pp
        elt.append(el)
    return elt
