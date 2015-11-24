import numpy as np
from scipy import interpolate

def eval_potential(eltj, x):
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
        Vx = interpolate.splev(x, eltj['V']) 
    else:
        print('Unknown Potential Type')
    return Vx
