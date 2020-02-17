import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def gaussian(x, a, m, s, o):    # Gaussian to fit to
    gauss = a*np.exp(-.5*((x-m)/s)**2)+o
    return gauss


def gaussFit(x, y):             # Fit the gaussian and return parameters
    inits = [max(y), 350, 10, np.mean(y)]
    params, covar = curve_fit(gaussian, x, y, p0=inits)
    return params


def getCoData(theta):             # Load data from file, using the angle tag in file name. Returns integrated counts
    fname = '../data/Co60_DetC_{0}_2.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))

    fit = gaussFit(bins[200:400], data[200:400])
    #integral = quad(gaussian, fit[1]-3*fit[2], fit[1]+3*fit[2], args=(fit[0], fit[1], fit[2], fit[3]))[0]

    plt.bar(bins[200:400], data[200:400], width=1, label='Scintillator Data')
    plt.plot(bins[200:400], gaussian(bins[200:400], *fit), 'r--', label='Gaussian Fit')
    plt.xlabel('Time Delay Bin Number')
    plt.ylabel('Coincidence Counts')
    plt.title('$^{60}$Co Coincidence Histogram at '+str(theta)+'$^\circ$ for a Live Time of 206.4 Seconds')
    plt.xlim(200, 400)
    plt.legend()
    plt.show()
    return


def getNaData(theta):
    fname = '../data/Na22_DetC_{0}.txt'.format(str(theta).zfill(2))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))

    fit = gaussFit(bins[330:360], data[330:360])
    domain = np.linspace(330, 360, 200)

    plt.bar(bins[330:360], data[330:360], width=1, label='Scintillator Data')
    plt.plot(domain, gaussian(domain, *fit), 'r--', label='Gaussian Fit')
    plt.xlabel('Time Delay Bin Number')
    plt.ylabel('Coincidence Counts')
    plt.title('$^{22}$Na Coincidence Histogram at '+str(theta)+'$^\circ$ for a Live Time of 304.98 Seconds')
    plt.xlim(330, 360)
    plt.legend()
    plt.show()
    return


getCoData(30)
getNaData(5)
