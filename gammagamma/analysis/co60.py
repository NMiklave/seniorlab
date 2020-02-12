import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def gaussian(x, a, m, s, o):
    gauss = a*np.exp(-.5*((x-m)/s)**2)+o
    return gauss


def gaussFit(x, y):
    inits = [max(y), 350, 10, np.mean(y)]
    params, covar = curve_fit(gaussian, x, y, p0=inits)
    return params


def getData(theta):
    fname = '../data/Co60_DetC_{0}_2.Spe'.format(str(theta).zfill(3))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))
    data = np.column_stack([bins, data])

   # plt.plot(*data[200:400].T)

    fit = gaussFit(*data[200:400].T)

    integral = quad(gaussian, fit[1]-3*fit[2], fit[1]+3*fit[2], args=(fit[0], fit[1], fit[2], fit[3]))[0]
   # plt.axvline(x=fit[1]-3*fit[2])
   # plt.axvline(x=fit[1]+3*fit[2])
   # plt.show()

    sum_noBG = sum(data[100:400].T[1]) - fit[3]*201

    print('Angle: ', theta)
    print(integral, sum_noBG)
    print('Delta: ', integral-sum_noBG)
    return integral


def legendre(x, a0, a1, a2, a3, a4):
    p1 = x
    p2 = .5*(3*x**2-1)
    p3 = .5*(5*x**3-3*x)
    p4 = .125*(35*x**4-30*x**2+3)
    func = a0*(1+a1*p1+a2*p2+a3*p3+a4*p4)
    return func


def fit_legendre(x, y, yerr):
    params, covar = curve_fit(legendre, x, y, sigma=yerr)
    range = np.linspace(x[0], x[-1], 200)
    plt.plot(range, legendre(range, *params),
             label='a0={0:2.4f}\na1={1:2.4f}\na2={0:2.4f}\na3={1:2.4f}\na4={2:2.4f}'.format(*params))
    return


def main():
    angles = np.arange(0, 140, 10)
    times = np.array([258.40, 239.66, 214.96, 206.40, 207.62, 201.98, 204.20,
                      205.92, 210.76, 202.50, 217.48, 213.40, 203.26, 213.74])
    counts = np.array([])
    for angle in angles:
        counts = np.append(counts, getData(angle))

    plt.errorbar(angles, counts/times, yerr=np.sqrt(counts)/times, fmt='k.', ecolor='g', capsize=3, capthick=1)
    fit_legendre(angles, counts/times, np.sqrt(counts)/times)
    plt.title("$^{60}$Co Coincidence Rate v. Detector Angle")
    plt.xlabel("Angle $(^\circ)$")
    plt.ylabel("Rate (counts/sec)")
    plt.legend()
    plt.savefig('../plots/co60.eps', format='eps')

    return


main()
