import numpy as np
def eval_potential(elt,j, x):
    n = len(x)
    Vx = np.zeros(n)
    if elt[j]['Vtype'] == 'constant':
        for i in range (0,n):
            Vx[i] = elt[j]['V']
        return Vx
    else:
        return print('Unknown Potential Type')
    
