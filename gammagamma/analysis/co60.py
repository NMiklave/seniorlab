import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Ideas:
    Calc mean and sig of each histogram, plot +/- 3 sig range, see if summing that removes BG
    Cry
"""

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def getData(theta):             # Load data from file, using the angle tag in file name. Returns integrated counts
    fname = '../data/Co60_DetC_{0}_6.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))
    data = np.column_stack([bins, data])

#    plt.plot(*data.T)#350:590].T)
#    plt.plot(data.T[0], gaussian(data.T[0], *fit))
#    plt.show()

    return sum(data.T[1])


def legendre(x, a0, a1, a2, a3, a4):        # Legendre polynomial fit
    p1 = x
    p2 = .5*(3*x**2-1)
    p3 = .5*(5*x**3-3*x)
    p4 = .125*(35*x**4-30*x**2+3)
    func = a0*(1+a1*p1+a2*p2++a3*p3+a4*p4)
    return func


def fit_legendre(x, y, yerr):               # Find the polynomial fit parameters .102and plot them
    inits = [1, 0, 0.1, 0, 0.009]
    params, covar = curve_fit(legendre, np.cos(np.pi*x/180), y, sigma=yerr, p0=inits)   # Legendre actually is cos(x)
    domain = np.linspace(0, 140, 200)                                                   # Range for plotting
    plt.plot(domain, legendre(np.cos(np.pi*domain/180), *params), 'r--',                # Plot fit over range
             label='a0={0:2.4f}\na1={1:2.4f}\na2={0:2.4f}\na3={1:2.4f}\na4={2:2.4f}'.format(*params))
    plt.plot(domain, legendre(np.cos(np.pi*domain/180), params[0], 0, 0.102, 0, 0.0091), 'b:', label='Theory Curve')
    return


def main():
    angles = np.array([0, 20, 45, 75, 90, 105, 135])
    times = np.array([873.20, 773.08, 746.80, 752.32, 866.86, 659.90, 721.86])
    counts = np.array([])
    for angle in angles:
        counts = np.append(counts, getData(angle))
    rates = counts/times
    sig_rates = np.sqrt(counts)/times
    normed_rates = rates/rates[5]
    sig_normed_rates = [normed_rates[i]*np.sqrt((sig_rates[i]/rates[i])**2+(sig_rates[5]/rates[5])**2)
                        for i in range(len(rates))]

    plt.errorbar(angles, normed_rates, yerr=sig_normed_rates, fmt='k.', ecolor='g', capsize=3, capthick=1)
    fit_legendre(angles, normed_rates, sig_normed_rates)
    plt.title("$^{60}$Co Coincidence Rate v. Detector Angle")
    plt.xlabel("Angle $(^\circ)$")
    plt.ylabel("Rate (counts/sec) Normalized by Rate at $90^\circ$")
    plt.legend()
    #plt.savefig('../plots/co60.eps', format='eps')
    plt.show()
    return


main()
