from compute_resonances import compute_resonances
from compare_eigs import compare_eigs
import numpy as np

def checked_resonances(elt, neigs=0, tol=1e-6):
    """
    Compute resonances with two densities in order to check convergence.
    If the same answer occurs to within tol, accept the pole as converged.

    Inputs:
        elt   -- coarse mesh
        neigs -- number of poles desired? (default: 0 -> compute all)
        tol   -- match tolerance (default: 1e-6)

    Output:
        l     --

    """

    elt2 = elt[:]
    for i in range(len(elt)):
        elt2[i]['order'] = int(np.ceil(elt[i]['order'] * 1.5))

    l1 = compute_resonances(elt=elt, neigs=neigs)
    l2 = compute_resonances(elt=elt2, neigs=neigs)

    l = compare_eigs(l2, l1, tol)
    return l
