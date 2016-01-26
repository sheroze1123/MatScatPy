from form_operators import form_operators
from plane_forcing import plane_forcing
import numpy as np

def compute_scatter (elt, l):
    """
    Compute the scattered wave in response to a plane wave of the form exp(i*l*x)
    """
    (K0, K1, K2) = form_operators (elt, l)
    F = plane_forcing (elt, l)
    return np.linalg.solve((-l*l*K2 + 1.0j*l*K1 + K0), F)
