import numpy as np
from checked_resonances import checked_resonances
from square_well import square_well
from plotting import plot_potential1
import matplotlib.pyplot as plt


def squarepot(VV = np.array([0,1,0]), xx = np.array([-2, -1, 1, 2]), neigs = 40):
    """
    Compute resonances of a one-dimensional piecewise-constant potential.
    The value of the potential will be VV(i) on the interval ( xx(i), xx(i+1) ).

    Input:
      VV    -- Value of the potential on each interval
      xx    -- Coordinates of the interval endpoints
      neigs -- Max eigenvalues or resonances to be computed (default: 40)

    Output:
      l     -- Vector of resolved resonance poles in the lambda (wave number) plane
    """

    elt = square_well(xx, VV)

    f, axarr = plt.subplots(2)
    plot_potential1( VV, xx, axarr[0] )

    l = checked_resonances(elt, neigs)

    # #TODO: Fix plot point sizes
    l_full = checked_resonances(elt)
    axarr[1].scatter(l_full.real, l_full.imag)
    axarr[1].set_title('Pole locations')
    # plt.axis('equal')
    plt.show()

    return l

squarepot()
