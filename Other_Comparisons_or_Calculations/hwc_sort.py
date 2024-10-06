import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('sorted_data_esi.csv')

# Drop rows with NaN values in 'Probability' column
data = data.dropna(subset=['Probability'])
data = data.dropna(subset=['ESI'])

names = data['P_NAME'].tolist()

uniques = []
for i in range(0, len(names)):
    if i < 80:
        if names[i] not in ['Venus', 'Mars', 'Proxima Centauri b', 'Ross 128 b', 'GJ 1061 c', 'GJ 1061 d', 'GJ 273 b', "Teegarden's Star b", "Teegarden's Star c", 'GJ 1002 b', 'GJ 1002 c', 'GJ 667 C e', 'GJ 667 C f', 'Wolf 1069 b', 'TRAPPIST-1 d', 'TRAPPIST-1 e', 'TRAPPIST-1 f', 'TRAPPIST-1 g', 'TOI-700 d', 'TOI-700 e', 'LP 890-9 c', 'TOI-715 b', 'K2-3 d', 'K2-72 e', 'Kepler-1649 c', 'Kepler-296 e', 'Kepler-186 f', 'Kepler-1652 b', 'Kepler-1229 b', 'Kepler-62 f', 'Kepler-442 b', 'LHS 1140 b', 'TOI-700 b']:
            uniques.append([names[i], i+1])
print(uniques)

esi_values = data['ESI'].tolist()
rhp_values = data['Probability'].tolist()

plt.scatter(range(len(names)), rhp_values, color='red', label='RHP', s=10)
plt.scatter(range(len(names)), esi_values, color='blue', label='ESI', s=10)

plt.xlabel('Index')
plt.ylabel('Values')
plt.legend()
plt.title('RHP v.s. ESI')

plt.show()