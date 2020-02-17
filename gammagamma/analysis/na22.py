import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Fix title text to match TeX
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'

def getDataPoint(fname):
  #Get data point and error from .txt file fname
  data = []
  for item in open(fname,'r'):
    item = item.strip()
    if item != '':
      try:
        data.append(float(item))
      except ValueError:
        pass
  mean = sum(data)
  stddev = math.sqrt(mean)
  return mean, stddev

def plot(angle, rate, error):
  fig, ax = plt.subplots()
  ax.errorbar(angle, rate, yerr=error, fmt='k.', ecolor='g', capsize=3, capthick=1)
  ax.set_title("$^{22}$Na Coincidence Rate v. Detector Angle")
  ax.set_xlabel("Angle $(^\circ)$")
  ax.set_ylabel("Rate (counts/sec)")
  plt.savefig("../plots/na22.eps", format='eps')
  plt.show()
  return

def printData(time, count, rate, sig):
  df = pd.DataFrame(np.array([time, count, rate, sig]).T, columns=['Time', 'Counts', 'Rate', 'SigRate'])
  print(df.to_latex())
  return

def main():
  angles = [0,5,10,15,20,30,45,60,75,90]
  liveTimes = [301.36,304.98,305.54,300.78,303.20,305.42,302.12,310.26,302.30,204.48]
  means = []
  rates = []
  errors = []
  index = 0
  for angle in angles:
    fname = "../data/Na22_DetC_" + str(angle).zfill(2) + ".txt"
    mean, stddev = getDataPoint(fname)
    time = liveTimes[index]
    means.append(mean)
    rates.append(mean/time)
    errors.append(stddev/time)
    index += 1
#  plot(angles, rates, errors)
#  printData(liveTimes, means, rates, errors)


main()
