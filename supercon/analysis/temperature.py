import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def loadData_temp(omega):
    volt, curr = np.loadtxt('../data/dewar/{}_0mA.txt'.format(omega), unpack=True)
    return np.array([volt, curr])


def plotData(data, i):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    ax.plot(data[0]/10, data[1]/10)
    ax.set_xlabel('Voltage [V]')
    ax.set_ylabel('Current [V]')
    ax.set_title('Niobium Junction IV Curve at {} K'.format(str(temps[i])))
    ax.set_ylim(-3, 3)
    ax.set_xlim(-.05, .05)
    ax.grid()
    return


resistances = np.array([86, 432, 526, 702, 815, 979, 1077, 1143, 1204, 1364])
temps = np.array([23.50, 8.50, 7.50, 6.50, 5.50, 5.00, 4.00, 3.50, 3.00, 2.50])

# Values for finding I_C(Delta)
energy_gaps = np.array([0, .020, .023, .026, .027, .028, .0285, .0287, .0285, .0288])/10
delta_0 = 0.02865/10
T_crit = delta_0/1.76/8.67e-5       # 18.77 K
T_bar = temps/T_crit
delta_squared = np.cos(np.pi*T_bar*T_bar/2)
T_range = np.linspace(.1*T_crit, 25, 500)/T_crit


plt.plot(T_range, np.cos(np.pi*T_range**2/2), label='Theory Curve')
plt.plot(T_bar, energy_gaps/delta_0, 'rx', label=r'Measured Normalized Energy Gap $\frac{\Delta(T)}{\Delta(0)}$')
plt.title('Normalized Energy Gap as a Function of the Normlized Temperature')
plt.xscale('log')
plt.xlabel('Normalized Temperature')
plt.ylabel('Normalized Energy Gap')
plt.legend()

#for i in range(len(resistances)):
#    plotData(loadData_temp(resistances[i]), i)
#    plt.show()

#plt.plot(temps, energy_gaps, 'rx')
#plt.xscale('log')


plt.show()
