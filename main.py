from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
import numpy as np

def func(x, I_0, a, lamda, C):
    return I_0 * (np.sin(math.pi * a * np.sin(x) / lamda) / (math.pi * a * np.sin(x) / lamda)) ** 2 + C

def Read_Two_Column_File(file_name):
    with open(file_name, 'r') as data:
        # sensor position (meters)
        x = []
        # light intensity (volts)
        y = []
        for line in data:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))

    return x, y

x, y = Read_Two_Column_File('single_04.txt')

shift = 0.0654
x = [n - shift for n in x]
x = [math.atan(n / 1.05) for n in x]
# y = [n + 0.02 for n in y]

p0 = [0.67,0.04,0.000650, -0.007]
popt, pconv = curve_fit(func, x, y, p0)

plt.figure(0)
plt.plot(x, func(x, *popt), c = 'r')
plt.scatter(x, y, s = 10)
plt.title("Light Intensity versus Angle From Center")
plt.ylabel("Light Intensity (Volts)")
plt.xlabel("Angle (Radians)")

plt.figure(1)
res = []
for i in range(len(x)):
    res.append(y[i] - func(x[i], *popt))
plt.scatter(x, res, s=10)
plt.title("Residuals of Fit")
plt.ylabel("Light Intensity (Volts)")
plt.xlabel("Angle (Radians)")

plt.show()

chi_squared = 0
for i in range(len(x)):
    if (i != 0):
        chi_squared += ((y[i] - func(x[i], *popt)) / 0.007) ** 2
print(chi_squared / (len(x)  - 4))