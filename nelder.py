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

# Define the function f(x, y)
def f(x, y):
    return x**2 - 4*x + y**2 - y - x*y + 7

# Generate x and y values for the contour plot
x = np.linspace(-1, 5, 100)
y = np.linspace(-1, 4, 100)
X, Y = np.meshgrid(x, y)

# Calculate the function values for each (x, y) pair
Z = f(X, Y)

plt.figure(figsize=(11,7.5))

# Create the contour plot
levels = np.arange(np.min(Z), np.max(Z)+0.5, 0.5)
contours = plt.contour(X, Y, Z, levels=levels, cmap='viridis')
plt.clabel(contours, inline=True, fontsize=8)
plt.xlabel('$x$')
plt.ylabel('$y$')

# Add point to the plot
point0 = (3,2)
orange_point = plt.scatter(point0[0], point0[1], color='red', s=40, marker='x')
t = plt.text(point0[0] + 0.06, point0[1] + 0.06,r'$\mathrm{min}$', fontsize=17, color='red', weight='bold')

# Set limits for x and y axes
plt.xlim([-1, 4])
plt.ylim([-1, 3])

# Add a grid to the plot
plt.grid(True, which='both', linewidth=0.5, color='gray', alpha=0.5)
plt.xticks(np.arange(-1, 5, 1))
plt.yticks(np.arange(-1, 4, 1))


# Display the plot
#plt.show()

plt.savefig('VU/text/Images/nelder.png')
