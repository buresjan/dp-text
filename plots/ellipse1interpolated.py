import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import matplotlib as mpl

# set font parameters to render with LaTeX
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['font.size'] = 15

mpl.rcParams['xtick.major.size'] = 7 #set the value globally
mpl.rcParams['xtick.minor.size'] = 5 #set the value globally
mpl.rcParams['ytick.major.size'] = 7 #set the value globally

def interpolate(x, y, xi):
    f = interp1d(x, y, kind='linear')
    yi = f(xi)
    return yi

x = [2 * k for k in range(91)]

y = np.loadtxt("VU/text/plots/TKE1.txt", usecols=[0])

xi = np.linspace(0, 180, num=180, endpoint=True)
yi = interpolate(x, y, xi)

fig, ax = plt.subplots(figsize=(8, 6)) # set the figure size to 8x6

ax.plot(xi, yi, color='black'	)
ax.set_xlabel(r"$\theta$ [$^\circ$]")
ax.set_ylabel(r"$T^{\mathrm{C}}_{\mathrm{turb}}$ [m$^2$s$^{-2}$]")
ax.set_xlim(left=0, right=180)
ax.set_ylim(bottom=0, top=150)
ax.axvline(x=90.0, color='grey', linestyle='--', alpha=0.7)

# Add point to the plot
point = (89.9, 138.75)
ax.scatter(point[0], point[1], color='r', s=30, marker='o')
ax.text(point[0] + 2, point[1] + 0.5,r'$\mathrm{max}$', fontsize=14, color='r', weight='bold')

point1 = (0, 10.78)
point2 = (180, 10.78)
ax.scatter(point1[0], point1[1], color='magenta', s=30, marker='o')
ax.text(point1[0] + 2, point1[1] + 2.5,r'$\mathrm{min}$', fontsize=14, color='magenta', weight='bold')
ax.scatter(point2[0], point2[1], color='magenta', s=30, marker='o')
ax.text(point2[0] - 10, point2[1] + 2.5,r'$\mathrm{min}$', fontsize=14, color='magenta', weight='bold')


plt.savefig('VU/text/Images/elip1interpolated.pdf')
# plt.show()
