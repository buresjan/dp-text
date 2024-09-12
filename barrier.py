import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator, NullLocator
from matplotlib.gridspec import GridSpec


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    # "font.serif": ["Charter"],
})
#plt.rcParams['axes.linewidth'] = 0.28 #set the value globally
plt.rcParams['xtick.major.size'] = 7 #set the value globally
plt.rcParams['xtick.minor.size'] = 5 #set the value globally
plt.rcParams['ytick.major.size'] = 7 #set the value globally
#plt.rcParams['xtick.major.width'] = 0.28
#plt.rcParams['ytick.major.width'] = 0.28
#plt.rcParams['xtick.minor.width'] = 0.23
#plt.rcParams['ytick.minor.width'] = 0.23

SMALL_SIZE = 19
MEDIUM_SIZE = 21
BIG_SIZE = 23
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIG_SIZE)     # fontsize of the axes title	
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('xtick.major', pad=10)
plt.rc('ytick.major', pad=10)
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize


def f(x, r):
    if x <= 4 or r == 0:
        j = 0
    else:
        j = 1
    return 0.5*x + (r*j)/(x-4)

x1 = np.linspace(-4, 10, 1000)
x2 = np.linspace(4, 10, 1000)
r_values = [0, 0.5, 1.5, 2.5]

plt.figure(figsize=(12,6.8))

for i, r in enumerate(r_values):
    if r == 0:
        x = x1
        lw = 3.0
    else:
        x = x2
        lw = 2.0
    y = [f(xi, r) for xi in x]
    label = f'$r={r}$'
    plt.plot(x, y, label=label, linewidth=lw)


plt.axvline(x=4, linestyle='--', color='gray')
plt.xlabel(r'$x$')
plt.ylabel(r'$\phi(x,r)$')
plt.xlim([-2	, 10])
plt.ylim([-10, 40])
plt.legend(loc='upper right')
#plt.show()
plt.savefig('VU/text/Images/barrier.pdf')
