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

df.insert(loc=0, column='0', value=676*[0])

df = df.sort_values(by=['a', 'rotation'])

# Parse command line arguments for a and rot
a = float(sys.argv[1])
rot = float(sys.argv[2])

points = df[['a', 'rotation']].values
values = df['value'].values

# Interpolate the data at (a, rot)
itp_val = griddata(points, values, (a, rot), method='cubic')

# Write the interpolated value to a text file
with open('itp.txt', 'w') as f:
    f.write(str(itp_val))

# Print DataFrame
# df.to_csv(r'cas.txt', header=None, index=None, sep=' ', mode='a')

# # Define interpolation grid
# a_grid = np.linspace(0.08, 0.13, 100)
# rotation_grid = np.linspace(45, 120, 100)
# a_mesh, rotation_mesh = np.meshgrid(a_grid, rotation_grid)

# # Interpolate missing values
# points = df[['a', 'rotation']].values
# values = df['value'].values
# interpolated_values = griddata(points, values, (a_mesh, rotation_mesh), method='cubic')

# # Create 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(a_mesh, rotation_mesh, interpolated_values, cmap='viridis')
# ax.set_xlabel('a')
# ax.set_ylabel('rotation')
# ax.set_zlabel('value')
# plt.show()
