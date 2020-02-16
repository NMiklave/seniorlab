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


def getData(theta):             # Load data from file, using the angle tag in file name. Returns integrated counts
    fname = '../data/Co60_DetC_{0}_2.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))
    data = np.column_stack([bins, data])

    fit = gaussFit(*data[200:400].T)
    integral = quad(gaussian, fit[1]-3*fit[2], fit[1]+3*fit[2], args=(fit[0], fit[1], fit[2], fit[3]))[0]

    #plt.plot(*data[200:400].T)                 # If you want to view the gaussian fits
    #plt.plot(*data.T[0], )
    #plt.show()

    sum_noBG = sum(data[100:400].T[1]) - fit[3]*201

    print('Angle: ', theta)
    print(integral, sum_noBG)
    print('Delta: ', integral-sum_noBG)
    return integral


def legendre(x, a0, a1, a2, a3, a4):        # Legendre polynomial fit
    p1 = x
    p2 = .5*(3*x**2-1)
    p3 = .5*(5*x**3-3*x)
    p4 = .125*(35*x**4-30*x**2+3)
    func = a0*(1+a1*p1+a2*p2+a3*p3+a4*p4)
    return func


def fit_legendre(x, y, yerr):               # Find the polynomial fit parameters and plot them
    inits = [1, 0, 0.1, 0, 0.009]
    params, covar = curve_fit(legendre, np.cos(np.pi * x/180), y, sigma=yerr, p0=inits)     # Legendre actually is cos(x)
    domain = np.linspace(0, 140, 200)                                           # Range for plotting
    plt.plot(domain, legendre(np.cos(np.pi * domain/180), *params), 'r--',                  # Plot fit over range
             label='a0={0:2.4f}\na1={1:2.4f}\na2={0:2.4f}\na3={1:2.4f}\na4={2:2.4f}'.format(*params))
    return


def main():
    angles = np.arange(0, 140, 10)
    times = np.array([258.40, 239.66, 214.96, 206.40, 207.62, 201.98, 204.20,
                      205.92, 210.76, 202.50, 217.48, 213.40, 203.26, 213.74])
    counts = np.array([])
    for angle in angles:
        counts = np.append(counts, getData(angle))

    rates = counts/times
    sig_rates = np.sqrt(counts)/times
    normed_rates = rates/rates[9]
    sig_normed_rates = [normed_rates[i]*np.sqrt((sig_rates[i]/rates[i])**2+(sig_rates[9]/rates[9])**2)
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
