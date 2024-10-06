import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('data_folder_4/sorted_data.csv')

# Drop rows with NaN values in 'Probability' column
data = data.dropna(subset=['Probability'])

names = data['pl_name'].tolist()
values = data['Probability'].tolist()

# Plotting the values on a graph
plt.figure(figsize=(8, 6))
plt.scatter(range(len(values)), values, color='blue')

# Adding labels to the points
for i, (name, value) in enumerate(zip(names, values)):
  plt.text(i, value, name, fontsize=10, ha='right')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Values Plot')

# Show plot
plt.grid(True)
plt.show()
