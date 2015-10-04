import numpy as np
def problem_size(elt,nargout):
    N = 1;
    for k in range(0,len(elt)):
        N = N + elt[k]['order']
    if nargout ==2:
        nz = 0
        for k in range(0,len(elt)):
            nz = nz + (elt[k]['order'] + 1)**2
    return {'N':N,'nz':nz}
