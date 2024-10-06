import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('sorted_data_nasa.csv')

# Drop rows with NaN values in 'Probability' column
data = data.dropna(subset=['Probability'])

names = data['pl_name'].tolist()

uniques = []
for i in range(0, len(names)):
    if i < 80:
        if names[i] not in ['Earth', 'Mars', 'Proxima Centauri b', 'Ross 128 b', 'GJ 1061 c', 'GJ 1061 d', 'GJ 273 b', "Teegarden's Star b", "Teegarden's Star c", 'GJ 1002 b', 'GJ 1002 c', 'GJ 667 C e', 'GJ 667 C f', 'Wolf 1069 b', 'Trappist-1 d', 'Trappist-1 e', 'Trappist-1 f', 'Trappist-1 g', 'TOI-700 d', 'TOI-700 e', 'LP 890-9 c', 'TOI-715 b', 'K2-3 d', 'K2-72 e', 'Kepler-1649 c', 'Kepler-296 e', 'Kepler-186 f', 'Kepler-1652 b', 'Kepler-1229 b', 'Kepler-62 f', 'Kepler-442 b', 'LHS 1140 b', 'TOI-700 b']:
            uniques.append([names[i], i+1])
print(uniques)

values = data['Probability'].tolist()

# Plotting the values on a graph
plt.figure(figsize=(8, 6))
plt.scatter(range(len(values)), values, color='blue')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('RHP Plot')

# Show plot
plt.grid(True)
plt.show()