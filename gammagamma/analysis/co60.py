import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def getData(theta):             # Load data from file, using the angle tag in file name. Returns integrated counts
    fname = '../data/Co60_DetC_{0}_6.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))
    data = np.column_stack([bins, data])

    return sum(data.T[1])


def legendre(x, a0, a1, a2, a3, a4):        # Legendre polynomial fit
    p1 = x
    p2 = .5*(3*x**2-1)
    p3 = .5*(5*x**3-3*x)
    p4 = .125*(35*x**4-30*x**2+3)
    func = a0*(1+a1*p1+a2*p2+a3*p3+a4*p4)
    return func


def fit_legendre(x, y, yerr):               # Find the polynomial fit parameters .102and plot them
    inits = [1, 0, 0.1, 0, 0.009]
    params, covar = curve_fit(legendre, np.cos(np.pi*x/180), y, sigma=yerr, p0=inits)   # Legendre actually is cos(x)
    errors = np.sqrt(np.diag(covar))
    domain = np.linspace(0, 140, 200)                                                   # Range for plotting
    plt.plot(domain, legendre(np.cos(np.pi * domain / 180), *params), 'r--', label='Polynomial Fit')
    plt.plot(domain, legendre(np.cos(np.pi * domain / 180),
                              params[0], params[1], params[2]/(.9125**2), params[3], params[4]/(.974**2)),
             'k--', label='Angular Smearing Corrected Fit')
    plt.plot(domain, legendre(np.cos(np.pi*domain/180), params[0], 0, 0.102, 0, 0.0091), 'b:', label='Theory Curve')

    #chi2(x, y, params, yerr)

    print('Opening angle corrected: ', params*(.9125*.974))
    print('a0={0:2.3f} $\pm${5:2.3f}\na1={1:2.3f} $\pm${6:2.3f}\na2={2:2.3f} $\pm${7:2.3f}\n'
          'a3={3:2.3f} $\pm${8:2.3f}\na4={4:2.3f} $\pm${9:2.3f}'.format(*params, *errors))
    print('Fixed a2 and a4: ', params[2]/(.9125**2), params[4]/(.974**2), ' err ', errors[2]/(.9125**2), errors[4]/(.974**2))
    return


def chi2(xdata, ydata, popt, sigma):
    r = ydata - legendre(np.cos(np.pi*xdata/180), *popt)
    print('Chisq data:')
    print(r, sigma)
    chisq = sum((r/sigma)**2)
    print(chisq)
    print()
    return


def main():
    angles = np.array([0, 20, 45, 75, 90, 105, 135])
    times = np.array([873.20, 773.08, 746.80, 752.32, 866.86, 659.90, 721.86])
    counts = np.array([])
    for angle in angles:
        counts = np.append(counts, getData(angle))
    rates = counts/times
    sig_rates = np.sqrt(counts)/times
    print(rates)
    normed_rates = rates/rates[5]
    sig_normed_rates = [normed_rates[i]*np.sqrt((sig_rates[i]/rates[i])**2+(sig_rates[5]/rates[5])**2)
                        for i in range(len(rates))]

    angles = np.array([0, 20, 47, 70, 90, 105, 139])

    plt.errorbar(angles, normed_rates, xerr=3, yerr=sig_normed_rates, fmt='k.', ecolor='g', capsize=3, capthick=1,
                 label='Normalized Rates')
    fit_legendre(angles, normed_rates, sig_normed_rates)
    plt.title("$^{60}$Co Coincidence Rate v. Detector Angle")
    plt.xlabel("Angle $(^\circ)$")
    plt.ylabel("Rate (counts/sec) Normalized by Rate at $90^\circ$")
    plt.legend()
    #plt.savefig('../plots/co60_fit.eps', format='eps')
    plt.show()
    return


main()
