import numpy as np

def problem_size(elt):
    """
    Get total number of points in the mesh
    """

    N = sum(el['order'] for el in elt) + 1;
    nz = sum( (el['order'] + 1)**2 for el in elt)
    return (N, nz)
