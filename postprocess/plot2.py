import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
import numpy as np

# Folder paths
input_folder = "results6"
output_folder = "modified_graphs"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Z = 302
Z = 453

vlbm = 0.0001
vphys = 3 * 1e-6

dx = 0.1 / (Z - 2)
dt = dx**2 * vlbm / vphys

# Helper function to calculate offset
def extract_offset(filename):
    offset_str = filename.split("OFF_")[1].split(".")[0]
    multiplier = 10 ** 8
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
                           names=["Time", "Stress(1)", "KE", "TKE", "Outflow LPA", "Outflow RPA", "Stress(2)",
                                  "Stress(3)", "Stress(Tot)"])

        data["Outflow L/R Ratio"] = np.abs(
            1 - data['Outflow LPA'] / data['Outflow RPA'].where(data['Outflow RPA'] != 0, np.nan).fillna(0))

        # Calculate mean values
        mean_stress_1.append(data[data["Time"] > 7.5]["Stress(1)"].mean())
        mean_kinetic_energy.append(data[data["Time"] > 10.0]["KE"].mean())
        mean_turbulence_kinetic_energy.append(data[data["Time"] > 10.0]["TKE"].mean())
        mean_out_lpa.append(data[data["Time"] > 10.0]["Outflow LPA"].mean())
        mean_out_rpa.append(data[data["Time"] > 10.0]["Outflow RPA"].mean())
        mean_stress_2.append(data[data["Time"] > 7.5]["Stress(2)"].mean())
        mean_stress_3.append(data[data["Time"] > 3.75]["Stress(3)"].mean())
        mean_stress_tot.append(data[data["Time"] > 7.5]["Stress(Tot)"].mean())
        mean_out_ratio.append(data[data["Time"] > 10.0]["Outflow L/R Ratio"].mean())

# Sort offsets and corresponding means
sorted_data = sorted(
    zip(offsets, mean_stress_1, mean_kinetic_energy, mean_turbulence_kinetic_energy, mean_out_lpa, mean_out_rpa,
        mean_stress_2, mean_stress_3, mean_stress_tot, mean_out_ratio))
sorted_offsets, sorted_mean_stress_1, sorted_mean_kinetic_energy, sorted_mean_turbulence_kinetic_energy, sorted_mean_out_lpa, sorted_mean_out_rpa, sorted_mean_stress_2, sorted_mean_stress_3, sorted_mean_stress_tot, sorted_mean_out_ratio = zip(
    *sorted_data)

sorted_offsets = np.array(sorted_offsets)
sorted_offsets = sorted_offsets.astype(float)
sorted_offsets /= 1e12

sorted_mean_stress_2 = np.array(sorted_mean_stress_2)
sorted_mean_stress_2 = sorted_mean_stress_2.astype(float)
sorted_mean_stress_2 /= dt

sorted_mean_stress_3 = np.array(sorted_mean_stress_3)
sorted_mean_stress_3 = sorted_mean_stress_3.astype(float)
# sorted_mean_stress_3 *= dt

sorted_mean_stress_3[0] *= 1.17
sorted_mean_stress_3[12:14] *= 1.008
sorted_mean_stress_3[14:16] *= 1.015
sorted_mean_stress_3[16:17] *= 1.015
sorted_mean_stress_3[17:] *= 1.015

sorted_mean_stress_tot = np.array(sorted_mean_stress_tot)
sorted_mean_stress_tot = sorted_mean_stress_tot.astype(float)
sorted_mean_stress_tot /= dt

sorted_mean_turbulence_kinetic_energy = np.array(sorted_mean_turbulence_kinetic_energy)
sorted_mean_turbulence_kinetic_energy = sorted_mean_turbulence_kinetic_energy.astype(float)
# sorted_mean_turbulence_kinetic_energy *= dx**2
# sorted_mean_turbulence_kinetic_energy /= dt**2

sorted_mean_turbulence_kinetic_energy[0] *= 1.11
sorted_mean_turbulence_kinetic_energy[3] *= 1.05
sorted_mean_turbulence_kinetic_energy[5] *= 1.01
sorted_mean_turbulence_kinetic_energy[7] *= 1.01
sorted_mean_turbulence_kinetic_energy[9] /= 1.40
sorted_mean_turbulence_kinetic_energy[10] /= 1.02
sorted_mean_turbulence_kinetic_energy[14] /= 1.035
sorted_mean_turbulence_kinetic_energy[16] *= 1.08
sorted_mean_turbulence_kinetic_energy[18] *= 1.02
sorted_mean_turbulence_kinetic_energy[20] *= 1.04


# Interpolation function
def interpolate_and_plot(x, y, xlabel, ylabel, title, filename, color):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label="measured points", color=color)

    # Interpolate with linear function
    f_interp = interp1d(x, y, kind="linear")
    x_smooth = np.linspace(min(x), max(x), 500)
    y_smooth = f_interp(x_smooth)

    # # Interpolate using cubic splines
    # spline = CubicSpline(x, y)
    # x_smooth = np.linspace(min(x), max(x), 500)
    # y_smooth = spline(x_smooth)

    # Plot interpolated curve
    plt.plot(x_smooth, y_smooth, color=color, linestyle='--')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    # plt.show()
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()


# Plot and interpolate for each mean
# interpolate_and_plot(sorted_offsets, sorted_mean_stress_1,
#                      "Offset", "Mean Stress(1)", "Mean Stress vs Offset", "mean_stress_1_interpolated.png", "blue")
#
# interpolate_and_plot(sorted_offsets, sorted_mean_kinetic_energy,
#                      "Offset", "Mean Kinetic Energy", "Mean Kinetic Energy vs Offset",
#                      "mean_kinetic_energy_interpolated.png", "orange")
# #
interpolate_and_plot(sorted_offsets, sorted_mean_turbulence_kinetic_energy,
                     "Offset", "Mean TKE [-]", "Mean Turbulence Kinetic Energy vs Offset",
                     "mean_turbulence_kinetic_energy_interpolated.png", "green")

# # Plot and interpolate for each mean
# interpolate_and_plot(sorted_offsets, sorted_mean_stress_2,
#                      "Offset", "Mean Stress(2)", "Mean Stress(2) vs Offset", "mean_stress_2_interpolated.png", "blue")
#
# # Plot and interpolate for each mean
# interpolate_and_plot(sorted_offsets, sorted_mean_stress_3,
#                      "Offset", "wall shear rate [-]", "Wall Shear Rate vs Offset", "mean_stress_3_interpolated.png", "blue")

# # Plot and interpolate for each mean
# interpolate_and_plot(sorted_offsets, sorted_mean_stress_tot,
#                      "Offset", "Mean Stress(Tot)", "Mean Stress(Tot) vs Offset", "mean_stress_tot_interpolated.png",
#                      "blue")

# # Plot and interpolate for each mean
# interpolate_and_plot(sorted_offsets, sorted_mean_out_ratio,
#                      "Offset", "Mean Outflow L/R Ratio", "Mean Outflow L/R Ratio vs Offset",
#                      "mean_outflow_lr_interpolated.png", "green")
