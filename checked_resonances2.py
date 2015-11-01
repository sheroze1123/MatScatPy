from compute_resonances import compute_resonances
from compare_eigs import compare_eigs
from problem_size import problem_size
import numpy as np

def checked_resonances2(elt, neigs=0, tol=1e-6):
    """
    Compute resonances with two densities in order to check convergence.
    If the same answer occurs to within tol, accept the pole as converged.
    Inputs:
      elt   - coarse mesh
      neigs - number of poles desired? (default: 0 -> compute all)
      tol   - absolute estimated error tolerance (default: 1e-6)
              Use tol = 0 to return everything
    """

    (l, V) = compute_resonances(elt, neigs)
    if neigs == 0:
        neigs = len(l)
    N = problem_size(elt)
    dl = np.zeros((neigs,1))
    V = V[0:N,:]

    for k in range(0,neigs):
        dl[k] = errest_resonance(elt, l[k], V[:,k])

    if tol > 0:
        # Filter eigenvalues
        is_good = np.abs(dl) < tol
        l  = l[is_good]
        dl = dl[is_good]
        V  = V[:,is_good]

def errest_resonance(elt, l, psi):
    """
    Estimate the sensitivity of the resonance calculation.
    Input:
      elt - Mesh data structure
      l   - Computed eigenvalue
      psi - Computed wave function

    Output:
      dl  - Approximate error computed from linearized perturbation theory

    FIXME: I ought to make the chebdifft2 indexing convention equivalent
    (and the clencurt convention) equivalent to the convention for cheb
    """

    Qpsi2  = 0;  # Accumulate the integral of psi^2
    QpsiR  = 0;  # Accumulate integral of psi*R, R = (H-l^2) psi

    base = 0;

    for j in range(0, len(elt)):
        order    = elt[j]['order']
        (xf, wf) = clencurt(5*order)
        xf       = xf[::-1]
        xf       = elt[j]['a'] * (1 - xf)/2 + elt[j]['b'] * (1 + xf)/2
        wf       = wf * (elt[j]['b'] - elt[j]['a']) / 2;
        Vf       = eval_potential(elt[j], xf)

        I = np.arange(base,base+order)
        (dpsif, psif) = chebdifft2(psi(I), 2, 5*order+1)
        dpsif = dpsif * 4 / (elt[j]['b'] - elt[j]['a'])**2
        Rf = -dpsif + np.multiply(Vf, psif) - l*l*psif;

        Qpsi2 = Qpsi2 + wf * np.power(psif, 2)
        QpsiR = QpsiR + wf * np.multiply(psif, Rf)

        base = base + order

    dl = QpsiR / (2*l*Qpsi2 + 1j*(psi[0]**2 + psi[-1]**2));


def clencurt(N):
    """
    CLENCURT  nodes x (Chebyshev points) and weights w
          for Clenshaw-Curtis quadrature
    """
    theta = (np.pi * np.arange(0,N+1) / N).T
    x = np.cos(theta)
    w = np.zeros((N+1,))
    ii = np.arange(1,N)
    v = np.ones((N-1,))

    if N%2 == 0:
        w[0] = 1.0/(N**2 - 1)
        w[N] = w[0]
        for k in range(1, N/2):
            v = v - 2 * np.cos( 2 * k * theta[ii])/(4*k*k - 1)
        v = v - np.cos(N*theta[ii])/(N * N - 1)
    else:
        w[0] = 1.0/(N**2)
        w[N] = w[0]
        for k in range(1, (N-1)/2 + 1):
            v = v - 2 * np.cos(2 * k * theta[ii])/(4*k*k - 1)

    w[ii] = 2.0 * v / N
    return (x, w)
