import csv
import pandas as pd

class ExoplanetClimate:
    def __init__(self, data):
        self.data = data
        
    def calculate_temperature(self):  #done
        # Simplified calculation of planetary temperature
        self.surf_temperature = 1.33 * float(self.data['eq_temp']) - 51.93     #From line of best fit from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7580787/
        return self.surf_temperature
    
    def determine_seasons(self):   #done
        # Simplified determination of seasons based on orbital period
        if (10 <= float(self.data['pl_obliq']) <= 25) or (0 <= float(self.data['pl_orbeccen']) <= 0.25):  
            return "Planet experiences seasons similar to earth"
        elif (25 < float(self.data['pl_obliq']) <= 40) or (0.25 < float(self.data['pl_orbeccen']) < 1):  
            return "Planet experiences extreme seasons"
        else:
            return "Planets' seasons are so invariable that its fasrthest point from star will result in total freeze, thus removing any possibiltiy of life"
    
    def predict_precipitation(self):
        #calculate prediction from atmosphere elements like hdrogen, oxygen, etc...  --- Future steps
        # Simplified prediction of precipitation based on temperature and atmospheric moisture
        if self.surf_temperature > 273 :  # 0C which is freezing point of water, so water can still be in ice form.  
            self.precipitation = 0.3          #idk
            return "Expect precipitation"
        else:
            self.precipitation = 0.1     #idk
            return "Expect dry conditions"
        

# Read data from CSV file
df = pd.read_csv('earth_like.csv')

atmospheric_moisture = 0.7  # Example atmospheric moisture level

# Create an instance of ExoplanetClimate
exoplanets = {}
for index, row in df.iterrows():
    if ('N' in str(row['Primary Gases'])) or ('O' in str(row['Primary Gases'])):   #filterign through dataset so that surf_temp calcultaito nwill eb accurate
        exoplanet = ExoplanetClimate(row)
        exoplanets[row['pl_name']] = exoplanet

run = True
while run:
  user_in = input("Enter the name of the planet you want to know the estimated climate of: ")
  try:
    print(f'Climate predictions for {user_in}:')
    exoplanet = exoplanets[user_in]  

    # Calculate temperature
    temperature = exoplanet.calculate_temperature()
    print("Estimated temperature:", temperature, "K")

    # Determine seasons
    seasons = exoplanet.determine_seasons()
    print("Seasons:", seasons)

    # Predict precipitation
    precipitation = exoplanet.predict_precipitation()
    print("Precipitation prediction:", precipitation)

  except KeyError:
    print("Invalid Input")
  run = input("Would you like to continue? (y/n) ") == 'y'