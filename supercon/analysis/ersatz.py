import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

'''
TODO:
    Curve fit for resistances
    What is the curve one
    Why is one negative linear
'''

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def loadData(p, dec):
    volt, curr = np.loadtxt('../data/probe{}_IV.txt'.format(p), unpack=True)
    dcur, dang = np.loadtxt('../data/probe{}_angle.txt'.format(p), unpack=True)
    return np.array([volt, curr, dcur, dang])


def plotData(full_data, index):
    data = full_data[index]
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    fig.suptitle('Ersatz Probe {0}'.format(index+1))

    ax[0].plot(data[0], data[1], 'C0.')
    ax[0].set_xlabel('Voltage [V]')
    ax[0].set_ylabel('Current [V]')
    ax[0].set_title('IV Curve for Unknown Component')

    if index == 0:
        pass
    elif index == 3:
        fit_cubic(data[0], data[1], ax[0])
    else:
        fit_linear(data[0], data[1], ax[0])
    ax[0].legend()

    ax[1].plot(data[2], data[3], 'C0.', )
    ax[1].set_xlabel('Current [V]')
    ax[1].set_ylabel('Angle [Radians]')
    ax[1].set_title('Angle-Voltage Curve for Unknown Component')
    fig.tight_layout()
    return


def linear_model(x, a, b):
    return a+b*x


def cubic_model(x, a, b, c, d):
    return a+b*x+c*x**2+d*x**3


def fit_linear(x, y, axis):
    params, covar = curve_fit(linear_model, x, y)
    errors = np.sqrt(np.diag(covar))
    domain = np.linspace(x.min(), x.max(), 200)

    axis.plot(domain, linear_model(domain, *params), 'C1-',
              label='a={0:2.5f}$\pm${2:2.5f}\nb={1:2.5f}$\pm${3:2.5f}'.format(*params, *errors))
    return


def fit_cubic(x, y, axis):
    params, covar = curve_fit(cubic_model, x, y)
    errors = np.sqrt(np.diag(covar))
    domain = np.linspace(x.min(), x.max(), 200)

    axis.plot(domain, cubic_model(domain, *params), 'C1-',
              label='a={0:2.5f}$\pm${4:2.5f}\nb={1:2.5f}$\pm${5:2.5f}\nc={2:2.5f}$\pm${6:2.5f}\nd={3:2.5f}$\pm${7:2.5f}'.format(*params, *errors))
    return


def main():
    probes = [1, 2, 3, 4, 5]
    decades = [280, 280, 280, 280, 280]
    probe_data = []
    for i in range(len(probes)):
        probe_data.append(loadData(probes[i], decades[i]))

    for i in range(len(probes)):
        plotData(probe_data, i)

    plt.show()
    return


main()
