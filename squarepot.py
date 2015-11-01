import numpy as np
from checked_resonances import checked_resonances
from square_well import square_well
from plotting import plot_potential1
import matplotlib.pyplot as plt


# def squarepot(VV = np.array([0,1,0]), xx = np.array([-2, -1, 1, 2]), neigs = 40):
    # """
    # Compute resonances of a one-dimensional piecewise-constant potential.
    # The value of the potential will be VV(i) on the interval ( xx(i), xx(i+1) ).

    # Input:
      # VV    -- Value of the potential on each interval
      # xx    -- Coordinates of the interval endpoints
      # neigs -- Max eigenvalues or resonances to be computed (default: 40)

    # Output:
      # l     -- Vector of resolved resonance poles in the lambda (wave number) plane
    # """

VV = np.array([0,1,0])
xx = np.array([-2, -1, 1, 2])
neigs = 40
elt = square_well(xx, VV)
l = checked_resonances(elt, neigs)

f, axarr = plt.subplots(2)
plot_potential1( VV, xx, axarr[0] )

#TODO: Fix plot point sizes
axarr[1].plot(checked_resonances(elt))
axarr[1].title('Pole locations')
plt.show()
