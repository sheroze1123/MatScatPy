import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
# from matplotlib import rc

# rc('font',**{'family':'serif','serif':['Palatino']})
# rc('text', usetex=True)

from checked_resonances import checked_resonances
from square_well import square_well
from eval_potential import eval_potential
from problem_size import problem_size
from compute_scatter import compute_scatter

def plot_resonance(elt, neigs=0):
    fig, (ax1, ax2) = plt.subplots(2,1)
    (x,V) = plot_potential(elt)
    l = checked_resonances(elt, neigs)
    ax1.plot(x, V, marker='o', linestyle='-',color='r')
    ax1.set_title("Potential")
    ax2.plot(l.real, l.imag, marker='o', linestyle='',color='b')
    ax2.set_title("Pole locations")
    plt.show()

def plot_potential1(VV, xx, ax):
    """
    Plot the potential with continuous lines.
    """
    VV = np.pad(VV,(1,1),'constant')
    xx = np.append( np.append([2*xx[0] - xx[1]], xx), [2*xx[-1] - xx[-2]])
    yy = np.zeros(2 * len(xx))
    WW = np.zeros(2 * len(xx))
    yy[0:-1:2] = xx
    yy[1::2]   = xx
    WW[1:-2:2] = VV
    WW[2:-1:2] = VV

    #TODO: Fix plot point sizes
    ax.plot(yy, WW)
    ax.set_ylim([min(VV)-(max(VV)-min(VV))/3.0, max(VV)+(max(VV)-min(VV))/3.0])

# Returns the grid x to plot u
def plot_fields(elt, u):
    (N, _) = problem_size(elt)
    x_tot = None
    if len(u) > N:
        x_tot = np.zeros((N+len(elt)-1,))
    else:
        x_tot = np.zeros((N,))

    base = 0
    for el in elt:
        order = el['order']
        x = np.cos(np.pi * np.arange(order,-1,-1) / order)
        xelt = el['a'] * (1-x)/2 + el['b'] * (1+x)/2
        x_tot[base:base+order+1] = xelt
        if len(u) > N:
            base = base+order+1
        else:
            base = base+order

    return x_tot

def plot_potential(elt):
    nelt = len(elt)
    (N, _) = problem_size(elt)
    N += (len(elt) - 1)
    u = np.zeros((N,))
    x_tot = np.zeros((N,))
    base = 0
    for el in elt:
        order = el['order']
        x = np.cos(np.pi * np.arange(order,-1,-1) / order)
        xelt = el['a'] * (1-x)/2 + el['b'] * (1+x)/2
        x_tot[base:base+order+1] = xelt[:];
        u[base:base+order+1] = eval_potential(el, xelt)
        base = base+order+1
    return (x_tot, u)
    
def sq_potential(potentials):
    fig, (ax1, ax2) = plt.subplots(2,1)

    # intialize two line objects (one in each axes)
    line1, = ax1.plot([], [], marker='o', linestyle='',color='r')
    line2, = ax2.plot([], [], marker='o', linestyle='',color='b')
    line = [line1, line2]

    for ax in [ax1, ax2]:
        ax.set_ylim(-11, 1)
        ax.set_xlim(-2, 2)
        ax.grid()

    def data_gen():
        t = 0.0
        for pot in potentials:
            elt = square_well(ab=[-pot])
            (x,V) = plot_potential(elt)
            l = checked_resonances(elt, 20)
            yield x, V, l.real, l.imag

    def run(data):
        x, V, l_real, l_imag = data

        xmin = np.min(x) - 1
        xmax = np.max(x) + 1
        ax1.set_xlim(xmin, xmax)

        xmin = np.min(l_real) - 1
        xmax = np.max(l_real) + 1
        ymin = np.min(l_imag) - 1
        ymax = np.max(l_imag) + 1
        ax2.set_xlim(xmin, xmax)
        ax2.set_ylim(ymin, ymax)

        line[0].set_data(x, V)
        line[1].set_data(l_real, l_imag)
        ax1.figure.canvas.draw()
        ax2.figure.canvas.draw()
        return line

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,
        repeat=False)
    # ani.save('square_potential_well.mp4', bitrate=-1, dpi=200)
    plt.show()

def animate_wave(elt, ks, N=24):
    fig, (ax1, ax2) = plt.subplots(2,1)

    # intialize two line objects (one in each axes)
    line1, = ax1.plot([], [], marker='o', linestyle='',color='b')
    line2, = ax2.plot([], [], marker='o', linestyle='-',color='r')
    line = [line1, line2]

    for ax in [ax1, ax2]:
        ax.set_ylim(-2, 2)
        ax.set_xlim(elt[0]['a'], elt[-1]['b'])
        ax.grid()

    def data_gen():
        t = 0.0
        (x,V) = plot_potential(elt)
        for k in ks:
            title_str = r'Scattering from $\exp{(i * %g * \pi * x)}$'%k
            u = compute_scatter(elt, k*np.pi)
            umax = np.max(np.abs(u))
            for i in range(N):
                u_real = (u * np.exp(i*2.0j*np.pi/N)).real
                x_grid = plot_fields(elt, u)
                yield x, V, x_grid, u_real, title_str, umax

    def run(data):
        x, V, x_grid, u_real, title_str, umax = data

        ymin = np.min(V) - 1
        ymax = np.max(V) + 1
        ax1.set_ylim(ymin, ymax)

        xmin = np.min(x_grid) 
        xmax = np.max(x_grid) 
        ymin = -umax
        ymax =  umax
        ax2.set_ylim(ymin, ymax)
        ax2.set_title(title_str)

        line[0].set_data(x, V)
        line[1].set_data(x_grid, u_real)
        ax1.figure.canvas.draw()
        ax2.figure.canvas.draw()
        return line

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=200,
        repeat=False)
    # ani.save('animated_wave_sq_well.mp4', bitrate=-1, dpi=200)
    # ani.save('animated_wave_sq_well.gif', writer='imagemagick', fps=10)
    plt.show()
