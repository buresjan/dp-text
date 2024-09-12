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

print(max(df['value']))

# Define interpolation grid
a_grid = np.linspace(0.08, 0.13, 100)
rotation_grid = np.linspace(45, 120, 100)
a_mesh, rotation_mesh = np.meshgrid(a_grid, rotation_grid)

# Interpolate missing values
points = df[['a', 'rotation']].values
values = df['value'].values
interpolated_values = griddata(points, values, (a_mesh, rotation_mesh), method='cubic')






# iterate over the input files
for i in range(1, 4):
    # load the data from the input files
    # set font parameters to render with LaTeX
	plt.rcParams['text.usetex'] = True
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = ['Times New Roman']
	plt.rcParams['font.size'] = 21	

	plt.rcParams['xtick.major.size'] = 7 #set the value globally
	plt.rcParams['xtick.minor.size'] = 5 #set the value globally
	plt.rcParams['ytick.major.size'] = 7 #set the value globally


	#Create 2D intensity map
	fig, ax = plt.subplots(figsize=(8, 6))
#	intensity_map = ax.pcolormesh(a_mesh, rotation_mesh, interpolated_values, cmap='jet', alpha=0.65)
	intensity_map = ax.pcolormesh(a_mesh, rotation_mesh, interpolated_values, cmap='jet', alpha=1.0)
	ax.set_xlabel(r'$a$ [$\mathrm{m}$]', fontsize=20)
	ax.set_ylabel(r'$\mathrm{\theta}$ [$^\circ$]', fontsize=20)
	ax.yaxis.tick_right()
	ax.yaxis.set_label_position("right")
	ax.set_xlim([0.08, 0.13])
	#ax.set_xlim([0.08, 0.09])
	#ax.set_ylim([106, 116])
	ax.set_title(r'$\mathrm{}$', fontsize=17)
	#ax.grid(True)
	colorbar = fig.colorbar(intensity_map, location='left')
 
	colorbar.set_label(r"$T^{\mathrm{C}}_{\mathrm{turb}}$ [m$^2$s$^{-2}$]", fontsize=20)

	#Add point to the plot


	fig.tight_layout()
    
	with open(f"{i}.txt") as f1, open(f"{i+3}.txt") as f2:
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
	for row in data2:
	    x2.append(row[0])
	    y2.append(row[1])

	point0 = (x1[0], y1[0])
	point1 = (x1[-1], y1[-1])
	point2 = (x2[-1], y2[-1])
	
	o1a, o2a, o3a = (0.0, 0.0, 0.0)
	o1b, o2b, o3b = (0.0, 0.0, 0.0)
	
	
	if i == 1:
		text1 = r'\textbf{A}$_0$'
		text2 = r'\textbf{A}$^{\star}_{\mathbf{NM}}$'
		text3 = r'\textbf{A}$^{\star}_{\mathbf{L-BFGS}}$'

		o1a = -0.0025
		o2a = -0.00415
		o3a = -0.0051

		o1b = 3
		o2b = 3
		o3b = 3
	
	
	if i == 2:
		text1 = r'\textbf{B}$_0$'
		text2 = r'\textbf{B}$^{\star}_{\mathbf{NM}}$'
		text3 = r'\textbf{B}$^{\star}_{\mathbf{L-BFGS}}$'

		o1a = 0.003
		o2a = -0.0038
		o3a = -0.002

		o1b = 1
		o2b = 3.7
		o3b = -6
	
	if i == 3:
		text1 = r'\textbf{C}$_0$'
		text2 = r'\textbf{C}$^{\star}_{\mathbf{NM}}$'
		text3 = r'\textbf{C}$^{\star}_{\mathbf{L-BFGS}}$'

		o1a = -0.003
		o2a = -0.0038
		o3a = -0.0101

		o1b = 3
		o2b = 3
		o3b = 3
		
	
	orange_point = ax.scatter(point0[0], point0[1], color='deeppink', s=45, marker='x')
	ax.text(point0[0] + o1a, point0[1] + o1b, text1, fontsize=20, color='deeppink', weight='extra bold')

	orange_point = ax.scatter(point1[0], point1[1], color='black', s=40, marker='x')
	
	ax.text(point1[0] + o2a, point1[1] + o2b, text2, fontsize=20, color='black')

	orange_point = ax.scatter(point2[0], point2[1], color='black', s=40, marker='x')
	ax.text(point2[0] + o3a, point2[1] + o3b, text3, fontsize=20, color='black', weight='extra bold')


	# save the plot to a file
	plt.savefig(str(i) + "full.png")


	#plt.savefig('VU/text/Images/cassini2Dinterpolated.png')

	#plt.show()

