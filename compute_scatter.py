from form_operators import form_operators
from plane_forcing import plane_forcing
import numpy as np

def compute_scatter (elt, l):
    (K0, K1, K2) = form_operators (elt, l)
    F = plane_forcing (elt, l)
    return np.linalg.solve((-l*l*K2 + 1.0j*l*K1 + K0), F)
