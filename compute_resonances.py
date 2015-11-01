import numpy as np
from scipy.linalg import eigh

def compute_resonances(K0=None, K1=None, K2=None, neigs = 0):
    """
    Compute resonances via a generalized linear eigenvalue problem.

    Input:
        K0
        K1
        K2
        neigs -- Number of poles desired (default: 0 --> compute all)

    Output:
        l
        V
    """

    if K1 is not None and K2 is not None and K3 is None:
        neigs = K1

    if K1 is None and K2 is None and K3 is None:
        elt = K0
        (N, nnz) = problem_size(elt)
        issparse = (neigs != 0) and (nnz < 0.2 * N**2) and (N > 100)
        (K0, K1, K2) = form_operators(elt, issparse)

    N = len(K0)

    #TODO: Adding sparsity
    Z = np.zeros(N)
    I = np.eye(N)

    A = np.vstack( np.hstack((K0, Z)), np.hstack((Z, I)) )
    B = np.vstack( np.hstack((-K1, -K2)), np.hstack((I, Z)) )

    (l, V) = eigh(A, B)
    if neigs is 0:
        return (l, V)
    else:
        #TODO: Figure out LU decomposition and inverse iteration 
        #TODO: When sparse, use scipy.sparse.linalg to use linear operator
        return (l[:neigs], V[:,:neigs])
