import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd

df = pd.read_csv('earth_like.csv')

# Equilibrium temperatures (x-axis)
equilibrium_temps = df['eq_temp'][:24]   #first 80 percent fo dataset is for training

# Surface temperatures (y-axis)
surface_temps = df['T_surf'][:24]    #first 80 percent fo dataset is for training

# Planet names
planet_names = df['pl_name'][:24] #first 80 percent fo dataset is for training

# Plot data points with labels
plt.scatter(equilibrium_temps, surface_temps, label='Data Points')
for i, txt in enumerate(planet_names):
    plt.annotate(txt, (equilibrium_temps[i], surface_temps[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(equilibrium_temps, surface_temps)

# Calculate line of best fit
line_of_best_fit = slope * np.array(equilibrium_temps) + intercept

# Plot line of best fit
plt.plot(equilibrium_temps, line_of_best_fit, color='red', label='Line of Best Fit')

# Add labels and legend
plt.xlabel('Equilibrium Temperature (K)')
plt.ylabel('Surface Temperature (K)')
plt.title('Equilibrium Temperature vs. Surface Temperature')
plt.legend()

# Show plot
plt.grid(True)
plt.show()

# Print equation of line of best fit
print(f'Equation of Line of Best Fit: Surface Temperature = {slope:.2f} * Equilibrium Temperature + {intercept:.2f}')