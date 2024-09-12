import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import sys

# Load txt file with custom separator
df = pd.read_csv('VU/text/plots/cassini.txt', sep='_|\s+', header=None, engine='python')

# Rename columns
df.columns = ['a', 'rotation', 'value']

# Convert rotation and value to float
df[['rotation', 'value']] = df[['rotation', 'value']].astype(float)

df = df.sort_values(by=['a', 'rotation'])

print(max(df['value']))

# Define interpolation grid
a_grid = np.linspace(0.08, 0.13, 100)
rotation_grid = np.linspace(45, 120, 100)
a_mesh, rotation_mesh = np.meshgrid(a_grid, rotation_grid)

# Interpolate missing values
points = df[['a', 'rotation']].values
values = df['value'].values
interpolated_values = griddata(points, values, (a_mesh, rotation_mesh), method='cubic')



# set font parameters to render with LaTeX
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 15

plt.rcParams['xtick.major.size'] = 7 #set the value globally
plt.rcParams['xtick.minor.size'] = 5 #set the value globally
plt.rcParams['ytick.major.size'] = 7 #set the value globally


#Create 2D intensity map
fig, ax = plt.subplots(figsize=(8, 6))
intensity_map = ax.pcolormesh(a_mesh, rotation_mesh, interpolated_values, cmap='jet', alpha=0.5)
ax.set_xlabel(r'$a$ [-]', fontsize=17)
ax.set_ylabel(r'$\mathrm{\theta}$ [$^\circ$]', fontsize=17)
ax.set_xlim([0.08, 0.13])
#ax.set_xlim([0.08, 0.09])
#ax.set_ylim([106, 116])
ax.set_title(r'$\mathrm{}$', fontsize=17)
#ax.grid(True)
colorbar = fig.colorbar(intensity_map)
colorbar.set_label(r"$T^{\mathrm{C}}_{\mathrm{turb}}$", fontsize=14)

#Add point to the plot
point0 = (0.1262, 96.09717667009011)
orange_point = ax.scatter(point0[0], point0[1], color='black', s=40, marker='x')
t = ax.text(point0[0] - 0.005, point0[1] + 2,r'$\mathrm{max}$', fontsize=17, color='black', weight='bold')

with open(f"VU/text/plots/_cass/2.txt") as f1, open(f"VU/text/plots/_cass/5.txt") as f2:
    data1 = [[float(x) for x in line.strip().split()] for line in f1]
    data2 = [[float(x) for x in line.strip().split()] for line in f2]
    
    # extract x and y values for each staircase function
    x1 = []
    y1 = []
    for row in data1:
        x1.append(row[0])
        y1.append(row[1])
        
    x2 = []
    y2 = []
    prev_y2 = 0
    for row in data2:
        x2.append(row[0])
        y2.append(row[1])
        
for i in range(0,33):
    try:
	    ax.plot([x1[i], x1[i+1]], [y1[i], y1[i+1]], color='black', linewidth='3')
	    #t = ax.text(x1[i] + 0.001, y1[i] + 2,f"${i}$", fontsize=17, color='black', weight='bold')
    except:
	    pass
    try:
	    ax.plot([x2[i], x2[i+1]], [y2[i], y2[i+1]], color='magenta', linewidth='3')
    except:
	    pass

fig.tight_layout()

#plt.savefig('VU/text/Images/cassini2Dinterpolated.png')

plt.show()
