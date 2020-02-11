import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit
from scipy.integrate import quad

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
    fname = '../data/Co60_DetC_{0}.Spe'.format(str(theta).zfill(2))
    data = np.loadtxt(fname, skiprows=12, max_rows=2047)
    bins = np.arange(len(data))
    data = np.column_stack([bins, data])

    fit = gaussFit(*data[200:400].T)
    integral = quad(gaussian, 200, 400, args=(fit[0], fit[1], fit[2], 0))[0]
    sum_noBG = sum(data[200:400].T[1]) - fit[3] * 201

    print('Angle: ', theta)
    print('Delta: ', quad(gaussian, 200, 400, args=(fit[0], fit[1], fit[2], 0))[0]-sum_noBG)
    return integral


def main():
    angles = np.arange(0, 90, 10)
    data = []
    for angle in angles:
        data.append(getData(angle))

    plt.errorbar(angles, data, yerr=np.sqrt(data), fmt='k.', ecolor='g', capsize=3, capthick=1)
    plt.title("$^{60}$Co Coincidence Rate v. Detector Angle")
    plt.xlabel("Angle $(^\circ)$")
    plt.ylabel("Rate (counts/sec)")
    plt.show()
    return


main()
