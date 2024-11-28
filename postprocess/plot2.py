import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np

# Folder paths
input_folder = "results"  # Replace with your input folder
output_folder = "graphs"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Helper function to calculate offset
def extract_offset(filename):
    offset_str = filename.split("OFF_")[1].split(".")[0]
    multiplier = 10**8
    if offset_str.startswith("M"):
        return -int(offset_str[1:]) * multiplier
    return int(offset_str) * multiplier

# Initialize lists to store mean values and offsets
offsets = []
mean_stress = []
mean_kinetic_energy = []
mean_turbulence_kinetic_energy = []
mean_fluctuations = []

# Process each file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_folder, filename)
        offset = extract_offset(filename)

        # Read the file
        try:
            data = pd.read_csv(file_path, delim_whitespace=True, header=None, 
                               names=["Time", "Stress", "Kinetic Energy", "Turbulence Kinetic Energy", "Outflow"])
        except pd.errors.EmptyDataError:
            print(f"Skipping empty file: {filename}")
            continue

        # Skip files with no valid data
        if data.empty or data.isna().all().all():
            print(f"Skipping file with no valid data: {filename}")
            continue

        # Remove NaN values
        data = data.dropna()

        # Skip if data becomes empty after removing NaNs
        if data.empty:
            print(f"Skipping file with only NaN values: {filename}")
            continue

        # Append offset
        offsets.append(offset)

        # Plot the data
        plt.figure(figsize=(10, 8))
        for i, col in enumerate(["Stress", "Kinetic Energy", "Turbulence Kinetic Energy", "Fluctuations"], start=1):
            plt.subplot(4, 1, i)
            plt.plot(data["Time"], data[col], label=col)
            plt.xlabel("Time")
            plt.ylabel(col)
            plt.legend()
        plt.tight_layout()
        graph_path = os.path.join(output_folder, f"{filename.replace('.txt', '.png')}")
        plt.savefig(graph_path)
        plt.close()

        # Calculate mean values
        mean_stress.append(data[data["Time"] > 7.5]["Stress"].mean())
        mean_kinetic_energy.append(data[data["Time"] > 7.5]["Kinetic Energy"].mean())
        mean_turbulence_kinetic_energy.append(data[data["Time"] > 10.0]["Turbulence Kinetic Energy"].mean())
        mean_fluctuations.append(data[data["Time"] > 10.0]["Outflow"].mean())
        
print(mean_stress)
print(mean_kinetic_energy)
print(mean_turbulence_kinetic_energy)
print(mean_fluctuations)

# Sort offsets and corresponding means
sorted_data = sorted(zip(offsets, mean_stress, mean_kinetic_energy, mean_turbulence_kinetic_energy, mean_fluctuations))
sorted_offsets, sorted_mean_stress, sorted_mean_ke, sorted_mean_tke, sorted_mean_fluctuations = zip(*sorted_data)

# Interpolation and plotting function
def interpolate_and_plot(x, y, xlabel, ylabel, title, filename, color):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label="Data Points", color=color)
    
    # Interpolate using cubic splines
    spline = CubicSpline(x, y)
    x_smooth = np.linspace(min(x), max(x), 500)
    y_smooth = spline(x_smooth)
    
    # Plot interpolated curve
    plt.plot(x_smooth, y_smooth, label="Interpolated Curve", color=color, linestyle='--')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()

# Plot and interpolate for each mean
interpolate_and_plot(sorted_offsets, sorted_mean_stress, 
                     "Offset", "Mean Stress", "Mean Stress vs Offset", "mean_stress_interpolated.png", "blue")

interpolate_and_plot(sorted_offsets, sorted_mean_ke, 
                     "Offset", "Mean Kinetic Energy", "Mean Kinetic Energy vs Offset", "mean_kinetic_energy_interpolated.png", "orange")

interpolate_and_plot(sorted_offsets, sorted_mean_tke, 
                     "Offset", "Mean Turbulence Kinetic Energy", "Mean Turbulence Kinetic Energy vs Offset", 
                     "mean_turbulence_kinetic_energy_interpolated.png", "green")

interpolate_and_plot(sorted_offsets, sorted_mean_fluctuations, 
                     "Offset", "Mean Outflow", "Mean Outflow vs Offset", "mean_outflow_interpolated.png", "red")

