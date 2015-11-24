import numpy as np

def func_well(V, pts=np.arange(-1,2), order=20, *args):
    """
    elt = func_well(V, pts, order)

    Discretize a problem where the potential is given by a function handle
    Input:
      V     - potential function (or function list)
      pts   - element end points (default: -1:1)
      order - maximum element order (default: 20)
      args  - additional arguments to the potential function

    Additional arguments passed to func_well are passed on to the potential
    function V.
    """

    x = np.cos(np.pi * np.linspace(order,-1,-1) / float(order))
    elt = []
    
    for i in range(0,len(pts)-1):
        el = {}
        el['a'] = pts[i]
        el['b'] = pts[i+1]
        el['order'] = order

        if isinstance(V,list):
            el['V'] = V[i]
        else:
            el['V'] = V

        el['Vtype'] = 'function'
        el['args'] = args
        elt.append(el)

    return elt
