import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'


def loadData_temp(omega):
    volt, curr = np.loadtxt('../data/dewar/{}_0mA.txt'.format(omega), unpack=True)
    return np.array([volt, curr])


def plotData(data, i, R):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    ax.plot(data[0]/10, data[1]/10, 'rx')
    ax.plot([min(data[0]), max(data[0])], [R*min(data[0]), R*max(data[0])], 'k--')
    ax.set_xlabel('Voltage [V]')
    ax.set_ylabel('Current [V]')
    ax.set_title('Niobium Junction IV Curve at {} K'.format(str(temps[i])))
    ax.set_ylim(-.4, .4)
    ax.set_xlim(-.007, .007)
    ax.grid()
    return


resistances = np.array([86, 432, 526, 702, 815, 979, 1077, 1143, 1204, 1364])
temps = np.array([23.50, 8.50, 7.50, 6.50, 5.50, 5.00, 4.00, 3.50, 3.00, 2.50])
temp_err = 0.5
energy_gaps = np.array([0, .020, .023, .026, .027, .028, .0285, .0287, .0285, .0288])/10
energy_gap_err = 1e-7
current = [0, .028, .067, .080, .093, .109, .111, .109, .111, .122]
delta_0 = 0.02865/10            # Lowest 4 pts average (flattened)
delta_0_err = .5e-7


#
#   Critical Temp and energy gap as a function of T graph
#
def empirical_curve(t, tc):
    delta = np.sqrt(np.cos(np.pi/2*(t/tc)**2))
    return delta


params, errs = curve_fit(empirical_curve, temps[1:], energy_gaps[1:]/delta_0, p0=9,
                         sigma=energy_gaps[1:]/delta_0*np.sqrt((energy_gap_err/energy_gaps[1:])**2+(delta_0_err/delta_0)**2))
T_range = np.linspace(2, params, 500)

plt.plot(T_range, empirical_curve(T_range, params), label=r'Empirical Curve Fitting for $T_c$')
plt.errorbar(temps[1:], energy_gaps[1:]/delta_0, fmt='rx', xerr=temp_err,
             yerr=energy_gaps[1:]/delta_0*np.sqrt((energy_gap_err/energy_gaps[1:])**2+(delta_0_err/delta_0)**2),
             capsize=3,
             label=r'Measured Normalized Energy Gap $\frac{\Delta(T)}{\Delta(0)}$')
plt.title('Normalized Energy Gap as a Function of the Normalized Temperature')
plt.xlabel('Temperature [K]')
plt.ylabel('Normalized Energy Gap')
plt.legend()
plt.savefig('../figures/energy_gap.eps')
plt.close()


#
#   Find the critical current
#
def Ic_function(E, T, R):
    function = np.pi*E/2/R      # Amplitude factor, hidden divisor of electron charge to convert E to volts
    function *= np.tanh(E/(2*T*8.6e-5))
    return function


linear_data = loadData_temp(86)
max_index = np.argmax(linear_data[0])   
R_n = linear_data[1][max_index]/linear_data[0][max_index]
#for i in range(len(resistances)):
 #   plotData(loadData_temp(resistances[i]), i, R_n)
  #  plt.show()

plt.plot(T_range, Ic_function(empirical_curve(T_range, params)*1.76*8.6e-5*params, T_range, R_n)*1000, label='Theoretical Zero Point Current')
plt.plot(temps[1:], Ic_function(energy_gaps[1:], temps[1:], R_n)*1000, 'rx', label='Measured Zero Point Current')
plt.title('Zero Voltage Current as a Function of Junction Temperature')
plt.xlabel('Temperature [K]')
plt.ylabel('Zero Voltage Current [mA]')
plt.ylim([0, .065])
plt.xlim([2, 10])
plt.legend()
plt.savefig('../figures/zero_voltage_current.eps')
