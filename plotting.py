from matplotlib import *
import numpy as np

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
    
