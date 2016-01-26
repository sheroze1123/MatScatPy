import numpy as np
from problem_size import problem_size
from eval_potential import eval_potential

def plane_forcing (elt, l):
    """
    Compute a forcing vector corresponding to the influence of an 
    incident wave of the form exp(l*x)
    """

    z = l/1.0j
    (N, _) = problem_size(elt)
    F = np.zeros((N,), dtype='complex_')
    base = 0

    for el in elt:
        order = el['order']
        x = np.cos(np.pi * np.arange(order,-1,-1) / order)
        xelt = el['a'] * (1-x)/2.0 + el['b'] * (1+x)/2.0
        F[base:base+order+1] = -eval_potential(el, xelt) * np.exp(z*xelt)
        F[base] = 0
        F[base+order] = 0
        base = base+order

    return F
