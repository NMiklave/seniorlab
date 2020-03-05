import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    if dec == 280:
        volt, curr = np.loadtxt('../data/probe{}_IV.txt'.format(p), unpack=True)
        dcur, dang = np.loadtxt('../data/probe{}_angle.txt'.format(p), unpack=True)
    elif dec == 560:
        volt, curr = np.loadtxt('../data/probe{}_IV_560.txt'.format(p), unpack=True)
        dcur, dang = np.loadtxt('../data/probe{}_angle_560.txt'.format(p), unpack=True)
    else:
        return
    return np.array([volt, curr, dcur, dang])


def plotData(data):
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    ax[0].plot(data[0], data[1], 'g.')
    ax[0].set_xlabel('Voltage [V]')
    ax[0].set_ylabel('Current [V]')
    ax[0].set_title('IV Curve for Unknown Component')
    ax[1].plot(data[2], data[3], 'g.')
    ax[1].set_xlabel('Current [V]')
    ax[1].set_ylabel('Angle [Radians]')
    ax[1].set_title('Angle-Voltage Curve for Unknown Component')
    fig.tight_layout()
    plt.show()
    return


def main():
    probes = [1, 2, 3, 4, 5, 2, 3, 5]           # Hardcoded the repeats for other set from different decade resistor val
    decades = [280, 280, 280, 280, 280, 560, 560, 560]
    probe_data = []
    for i in range(len(probes)):
        probe_data.append(loadData(probes[i], decades[i]))

    plotData(probe_data[3])
    return


main()
