import numpy as np

def eval_potential(eltj, x):
    n = len(x)
    Vx = np.zeros(n)
    if eltj['Vtype'] == 'constant':
        Vx = eltj['V'] + 0 * x
    elif eltj['Vtype'] == 'function':
        Vx = -1 #TODO
    elif eltj['Vtype'] == 'spline':
        Vx = -1 #TODO
    else:
        print('Unknown Potential Type')
    return Vx
