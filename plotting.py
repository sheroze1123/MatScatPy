import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

from checked_resonances import checked_resonances
from square_well import square_well
from eval_potential import eval_potential
from problem_size import problem_size

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
    is_complex = (u.dtype == 'complex_')
    (N, _) = problem_size(elt)
    print N

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
    
# Subclassing example from http://matplotlib.org/examples/animation/subplots.html
class SquareWellPotential(animation.TimedAnimation):
    def __init__(self, potentials):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        self.potentials = potentials

        ax1.set_xlabel('x')
        ax1.set_ylabel('V(x)')
        ax1.set_title('Potential')
        self.line1 = Line2D([], [], color='red')
        ax1.add_line(self.line1)

        # ax1.set_xlabel('x')
        # ax1.set_ylabel('V(x)')
        ax2.set_title('Pole locations')
        # self.line2 = Line2D([], [], color='blue', marker='o')
        self.line2 = ax2.plot([], [], color='blue', marker='o')
        # ax2.add_line(self.line2)

        animation.TimedAnimation.__init__(self, fig, interval=50, blit=True, repeat=False)

    def _draw_frame(self, framedata):
        i = framedata
        elt = square_well(ab=[-self.potentials[i]])
        (x,u) = plot_potential(elt)
        print "X:"
        print x
        print "U:"
        print u
        l = checked_resonances(elt, 20)
        print "L:"
        print l
        # self.line2.set_data(x, u)
        self.line2.set_xdata(l.real)
        self.line2.set_ydata(l.imag)
        # self._drawn_artists = [self.line1, self.line2]
        self._drawn_artists = [self.line1]

    def new_frame_seq(self):
        return iter(range(self.potentials.size))

    def _init_draw(self):
        lines = [self.line1]
        for l in lines:
            l.set_data([], [])


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
        ymin = np.min(V) - 1
        ymax = np.max(V) + 1
        ax1.set_xlim(xmin, xmax)
        ax1.set_ylim(ymin, ymax)
        ax1.figure.canvas.draw()

        xmin = np.min(l_real) - 1
        xmax = np.max(l_real) + 1
        ymin = np.min(l_imag) - 1
        ymax = np.max(l_imag) + 1
        ax2.set_xlim(xmin, xmax)
        ax2.set_ylim(ymin, ymax)
        ax2.figure.canvas.draw()

        line[0].set_data(x, V)
        line[1].set_data(l_real, l_imag)
        return line

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,
        repeat=False)
    # ani.save('animation.mp4')
    plt.show()

def animate_wave(elt, ks, N=24):
    fig, (ax1, ax2) = plt.subplots(2,1)

    # intialize two line objects (one in each axes)
    line1, = ax1.plot([], [], marker='o', linestyle='',color='r')
    line2, = ax2.plot([], [], marker='o', linestyle='',color='b')
    line = [line1, line2]
    (x,V) = plot_potential(elt)

    for ax in [ax1, ax2]:
        ax.set_ylim(-11, 1)
        ax.set_xlim(-2, 2)
        ax.grid()

    def data_gen():
        t = 0.0
        for k in ks:
            for i in range(N):
                yield x, V, l.real, l.imag

    def run(data):
        x, V, l_real, l_imag = data

        xmin = np.min(x) - 1
        xmax = np.max(x) + 1
        ymin = np.min(V) - 1
        ymax = np.max(V) + 1
        ax1.set_xlim(xmin, xmax)
        ax1.set_ylim(ymin, ymax)
        ax1.figure.canvas.draw()

        xmin = np.min(l_real) - 1
        xmax = np.max(l_real) + 1
        ymin = np.min(l_imag) - 1
        ymax = np.max(l_imag) + 1
        ax2.set_xlim(xmin, xmax)
        ax2.set_ylim(ymin, ymax)
        ax2.figure.canvas.draw()

        line[0].set_data(x, V)
        line[1].set_data(l_real, l_imag)
        return line

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,
        repeat=False)
    # ani.save('animation.mp4')
    plt.show()
