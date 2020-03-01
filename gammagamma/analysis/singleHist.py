import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def getCoData(theta):             # Load data from file, using the angle tag in file name. Returns integrated counts
    fname = '../data/Co60_DetC_{0}_6.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))

    plt.bar(bins, data, width=1, label='Scintillator Data')
    plt.xlabel('Time Delay Signal Voltage')
    plt.xticks([])
    plt.yticks(range(0, 20, 3))
    plt.ylabel('Coincidence Counts')
    plt.title('$^{60}$Co Coincidence Histogram at '+str(theta)+'$^\circ$ for a Live Time of 659.90 Seconds')
    plt.xlim(0, 1250)
    plt.legend()
    plt.show()
    plt.savefig('../plots/co60_105deg.eps', format='eps')
    return


getCoData(105)
