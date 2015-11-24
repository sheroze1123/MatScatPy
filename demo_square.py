#
# Compute scattering states and resonances for a one-dimensional square well
# potential ("particle in a box").
#

# -- Example 1: Show dynamics of resonances changing to bound states --
import matplotlib
matplotlib.use('TKAgg')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from plotting import sq_potential
from plotting import plot_potential
from square_well import square_well
from compute_scatter import compute_scatter
from plotting import plot_fields

print 'In the first example, we show how the eigenvalues and resonances \
change as the depth of a square potential well changes.'
raw_input('Press Enter to begin\n')

potentials = np.linspace(6,10,20)
sq_potential(potentials)

print '\nNow we consider the scattering from a plane wave of the form exp(-ikx), where k = pi.  The real part of the scattered wave is in red; the imaginary part is in blue.'
raw_input('Press Enter to begin\n')
elt = square_well([-10])
u = compute_scatter(elt, -np.pi)
(x,V) = plot_potential(elt)
x_u = plot_fields(elt, u)
fig, (ax1, ax2) = plt.subplots(2,1)

# intialize two line objects (one in each axes)
line1, = ax1.plot(x, V, marker='o', linestyle='-',color='r')
line2, = ax2.plot(x_u, u.real, marker='o', linestyle='-',color='r')
line2, = ax2.plot(x_u, u.imag, marker='o', linestyle='-',color='b')
plt.show()

print 'In addition to just displaying the potential, we can also animate the wave -- that is, we show Re(exp(i*t)*u_s), where u_s is the scattered wave function.  We will show an animation for a range of wave numbers for the incident wave'
raw_input('Press Enter to begin\n')

ks = np.linspace(0.8,1.2,3)
animate_wave(ks)
