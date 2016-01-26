import numpy as np
from clampedspline import *

def eval_potential(eltj, x):
    """
    Evaluate the potential associated with the mesh element
    eltj at x
    """

    n = len(x)
    Vx = np.zeros(n)
    if eltj['Vtype'] == 'constant':
        Vx = eltj['V'] + 0 * x
    elif eltj['Vtype'] == 'function':
        if (len(eltj['args'])) > 0:
            Vx = eltj['V'](x, *eltj['args'])
        else:
            Vx = eltj['V'](x)

    elif eltj['Vtype'] == 'spline':
        Vx, DVx, DDVx = cubic_spline_evaluate(x, eltj['V'], eltj['xx'])
    else:
        print('Unknown Potential Type')
    return Vx
