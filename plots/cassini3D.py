import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import sys

# Load txt file with custom separator
df = pd.read_csv('cassini.txt', sep='_|\s+', header=None, engine='python')

# Rename columns
df.columns = ['a', 'rotation', 'value']

# Convert rotation and value to float
df[['rotation', 'value']] = df[['rotation', 'value']].astype(float)

df = df.sort_values(by=['a', 'rotation'])

# Define interpolation grid
a_grid = np.linspace(0.08, 0.13, 100)
rotation_grid = np.linspace(45, 120, 100)
a_mesh, rotation_mesh = np.meshgrid(a_grid, rotation_grid)

# Interpolate missing values
points = df[['a', 'rotation']].values
values = df['value'].values - 200.0
interpolated_values = griddata(points, values, (a_mesh, rotation_mesh), method='cubic')



# set font parameters to render with LaTeX
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 15

plt.rcParams['xtick.major.size'] = 7 #set the value globally
plt.rcParams['xtick.minor.size'] = 5 #set the value globally
plt.rcParams['ytick.major.size'] = 7 #set the value globally

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(a_mesh, rotation_mesh, interpolated_values, cmap='viridis', alpha=0.99)
plt.xlim([0.08, 0.125])
ax.set_xlabel(r'$a$ [-]')
ax.set_ylabel(r"$\alpha$ [$^\circ$]")
ax.set_zlabel(r"$T^{\mathrm{C}}_{\mathrm{turb}}$")


plt.show()
