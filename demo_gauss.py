import numpy as np
from func_well import func_well
from plotting import plot_resonance

def gauss_potential(x):
    return -10 * np.exp(-(3*x)**2)

print 'Compute resonances for a Gaussian potential well'
elt = func_well(gauss_potential, np.arange(-1,1.5,0.5), 30)
plot_resonance(elt,20)
