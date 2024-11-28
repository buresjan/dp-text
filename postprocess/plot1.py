import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
import numpy as np

# Folder paths
input_folder = "results"
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
mean_stress_1 = []
mean_kinetic_energy = []
mean_turbulence_kinetic_energy = []
mean_out_lpa = []
mean_out_rpa = []
mean_stress_2 = []
mean_stress_3 = []
mean_stress_tot = []
mean_out_ratio = []

# Process each file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_folder, filename)
        offset = extract_offset(filename)
        offsets.append(offset)

        # Read the file
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, 
                           names=["Time", "Stress(1)", "KE", "TKE", "Outflow LPA", "Outflow RPA", "Stress(2)", "Stress(3)", "Stress(Tot)"])

        data["Outflow L/R Ratio"] = np.abs(1 - data['Outflow LPA'] / data['Outflow RPA'].where(data['Outflow RPA'] != 0, np.nan).fillna(0))

        # Plot the data
        plt.figure(figsize=(12, 8))
        for i, col in enumerate(["Stress(1)", "KE", "TKE", "Stress(2)", "Stress(3)", "Stress(Tot)"], start=1):
            plt.subplot(6, 1, i)
            plt.plot(data["Time"], data[col], label=col)
            plt.xlabel("Time")
            plt.ylabel(col)
            plt.legend()
        plt.tight_layout()
        graph_path = os.path.join(output_folder, f"{filename.replace('.txt', '.png')}")
        plt.savefig(graph_path)
        plt.close()

        # Calculate mean values
        mean_stress_1.append(data[data["Time"] > 5.0]["Stress(1)"].mean())
        mean_kinetic_energy.append(data[data["Time"] > 10.0]["KE"].mean())
        mean_turbulence_kinetic_energy.append(data[(data["Time"] > 10.0) & (data["Time"] < 11.0)]["TKE"].mean())
        mean_out_lpa.append(data[data["Time"] > 10.0]["Outflow LPA"].mean())
        mean_out_rpa.append(data[data["Time"] > 10.0]["Outflow RPA"].mean())
        mean_stress_2.append(data[data["Time"] >  5.0]["Stress(2)"].mean())
        mean_stress_3.append(data[data["Time"] >  5.0]["Stress(3)"].mean())
        mean_stress_tot.append(data[data["Time"] >  5.0]["Stress(Tot)"].mean())
#        mean_stress_tot.append(data[(data["Time"] > 10.0) & (data["Time"] < 11.5)]["Stress(Tot)"].mean())
        mean_out_ratio.append(data[data["Time"] >  10.0]["Outflow L/R Ratio"].mean())

# Sort offsets and corresponding means
sorted_data = sorted(zip(offsets, mean_stress_1, mean_kinetic_energy, mean_turbulence_kinetic_energy, mean_out_lpa, mean_out_rpa, mean_stress_2, mean_stress_3, mean_stress_tot, mean_out_ratio))
sorted_offsets, sorted_mean_stress_1, sorted_mean_kinetic_energy, sorted_mean_turbulence_kinetic_energy, sorted_mean_out_lpa, sorted_mean_out_rpa, sorted_mean_stress_2, sorted_mean_stress_3, sorted_mean_stress_tot, sorted_mean_out_ratio = zip(*sorted_data)

# Interpolation function
def interpolate_and_plot(x, y, xlabel, ylabel, title, filename, color):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label="Data Points", color=color)
    
    # Interpolate
    #f_interp = interp1d(x, y, kind="linear")
    #x_smooth = np.linspace(min(x), max(x), 500)
    #y_smooth = f_interp(x_smooth)

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
interpolate_and_plot(sorted_offsets, sorted_mean_stress_1,
                     "Offset", "Mean Stress(1)", "Mean Stress vs Offset", "mean_stress_1_interpolated.png", "blue")

interpolate_and_plot(sorted_offsets, sorted_mean_kinetic_energy,
                     "Offset", "Mean Kinetic Energy", "Mean Kinetic Energy vs Offset", "mean_kinetic_energy_interpolated.png", "orange")

interpolate_and_plot(sorted_offsets, sorted_mean_turbulence_kinetic_energy,
                     "Offset", "Mean Turbulence Kinetic Energy", "Mean Turbulence Kinetic Energy vs Offset", 
                     "mean_turbulence_kinetic_energy_interpolated.png", "green")

# Plot and interpolate for each mean
interpolate_and_plot(sorted_offsets, sorted_mean_stress_2,
                     "Offset", "Mean Stress(2)", "Mean Stress(2) vs Offset", "mean_stress_2_interpolated.png", "blue")

# Plot and interpolate for each mean
interpolate_and_plot(sorted_offsets, sorted_mean_stress_3,
                     "Offset", "Mean Stress(3)", "Mean Stress(3) vs Offset", "mean_stress_3_interpolated.png", "blue")

# Plot and interpolate for each mean
interpolate_and_plot(sorted_offsets, sorted_mean_stress_tot,
                     "Offset", "Mean Stress(Tot)", "Mean Stress(Tot) vs Offset", "mean_stress_tot_interpolated.png", "blue")


# Plot and interpolate for each mean
interpolate_and_plot(sorted_offsets, sorted_mean_out_ratio,
                     "Offset", "Mean Outflow L/R Ratio", "Mean Outflow L/R Ratio vs Offset", "mean_outflow_lr_interpolated.png", "green")
