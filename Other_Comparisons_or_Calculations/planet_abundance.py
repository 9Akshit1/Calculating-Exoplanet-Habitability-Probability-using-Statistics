import pandas as pd
import math

def predict_planetary_composition(hypatia_values, distance_from_star):
  global elements

  similarity_factor = 1 - distance_from_star  # Closer planets have higher similarity
  composition = {}
  for i in range(0, len(hypatia_values)):
      # Adjust abundance based on distance from the star
      estimated_abundance = hypatia_values[i] * similarity_factor    #abundance * similarity_factor
      composition[elements[i]] = estimated_abundance

  return composition

def hb_zone(spectral_type, app_mag, sy_dist):
  
  BC_constants = {
    "O0": -4.46,
    "O1": -4.32,
    "O2": -4.03,
    "O3": -3.79,
    "O4": -3.46,
    "O5": -3.35,
    "O6": -3.28,
    "O7": -3.23,
    "O8": -3.10,
    "O9": -3.03,  #idf if O-type BC vals are correct
    
    "B0": -2.84,
    "B1": -2.58,
    "B2": -2.26,
    "B3": -1.85,
    "B4": -1.75,  #estimated
    "B5": -1.65,
    "B7": -1.40,
    "B8": -1.255,   #estimated
    "B9": -1.11,
    
    "A0": -0.68,
    "A1": -0.63,
    "A2": -0.56,
    "A3": -0.49,  #estimated
    "A4": -0.42,
    "A5": -0.32,  #estimated
    "A6": -0.23,
    "A7": -0.195,  #estimated
    "A8": -0.16,
    "A9": -0.13,  #estimated
    
    "F0": -0.10,
    "F1": -0.085,  #estimated
    "F2": -0.07,
    "F3": -0.085,  #estimated
    "F4": -0.10,
    "F5": -0.125,  #estimated
    "F6": -0.15,
    "F7": -0.18,   #estimated
    "F8": -0.21,
    "F9": -0.24,  #estimated
    
    "G0": -0.27,
    "G1": -0.305,  #estimated
    "G2": -0.34,
    "G3": -0.38,  #estimated
    "G4": -0.42,
    "G5": -0.46,   #estimated
    "G6": -0.50,
    "G7": -0.535,  #estimated
    "G8": -0.57,
    "G9": -0.605,  #estimated
    
    "K0": -0.64,
    "K1": -0.675,   #estimated
    "K2": -0.71,
    "K3": -0.74,   #estimated
    "K4": -0.77,
    "K5": -0.81,   #estimated
    "K6": -0.85,
    "K7": -0.89,   #estimated
    "K8": -0.97,
    "K9": -1.24,   #estimated
    
    "M0": -1.51,
    "M1": -2.395,   #estimated
    "M2": -3.28,
    "M3": -3.62,   #estimated
    "M4": -3.96,
    "M5": -4.26,
    "M6": -4.63,   #estimated
    "M7": -5.16,   #estimated
    "M8": -5.52,   #estimated
  }
  
  abs_mag = app_mag - 5*math.log10(sy_dist/10)  #calculate absolute magnitude
  bol_mag = abs_mag + BC_constants[spectral_type]
  rel_lumin = 10**((bol_mag - 4.72)/(-2.5)) 

  r_i = math.sqrt(rel_lumin/1.1)
  r_o = math.sqrt(rel_lumin/0.53)
  return r_i, r_o

def estimate_star_spect(effective_temperature):
  #Assuming they are all Main Sequence
  star_types = {
      "O0": 50000,
      "O1": 48000,
      "O2": 46000,
      "O3": 44000,
      "O4": 42000,
      "O5": 40000,
      "O6": 37000,
      "O7": 34000,
      "O8": 31000,
      "O9": 28000,   
    
      "B0": 25200,
      "B1": 23000,
      "B2": 21000,
      "B3": 17600,
      "B4": 16400,
      "B5": 15200,
      "B6": 14300,
      "B7": 13500,
      "B8": 12300,
      "B9": 11400,
  
      "A0": 9600,
      "A1": 9330,
      "A2": 9040,
      "A3": 8750,
      "A4": 8480,
      "A5": 8310,
      "A6": 8965,
      "A7": 7920,
      "A8": 7730,
      "A9": 7540,
  
      "F0": 7350,
      "F1": 7200,
      "F2": 7050,
      "F3": 6850,
      "F4": 6775,
      "F5": 6700,
      "F6": 6550,
      "F7": 6400,
      "F8": 6300,
      "F9": 6175,
  
      "G0": 6050,
      "G1": 5930,
      "G2": 5800,
      "G3": 5750,
      "G4": 5710,
      "G5": 5660,
      "G6": 5590,
      "G7": 5510,
      "G8": 5440,
      "G9": 5340,
  
      "K0": 5240,
      "K1": 5110,
      "K2": 4960,
      "K3": 4800,
      "K4": 4600,
      "K5": 4400,
      "K6": 4200,
      "K7": 4000,
      "K8": 8920,
      "K9": 3830,
  
      "M0": 3750,
      "M1": 3700,
      "M2": 3600,
      "M3": 3500,
      "M4": 3400,
      "M5": 3200,
      "M6": 3100,
      "M7": 2900,
      "M8": 2000
  }
  #ignoring L & T star spectrum because they aren't suitable for planet habitabiltiy anyway. TEMPS ARE FROM HERE: https://www.atnf.csiro.au/outreach/education/senior/astrophysics/photometry_colour.html
  closest_type = None
  min_difference = float('inf')

  for star_type, temperature in star_types.items():
      difference = abs(temperature - effective_temperature)
      if difference < min_difference:
          min_difference = difference
          closest_type = star_type

  return closest_type

df = pd.read_csv('hypatia2.csv')
# Initialize a list to store all planet data
all_data = {}
global elements
elements = ["Fe", "Li", "C", "N", "O", "Na", "Mg", "Al", "Si", "P", "S", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Co", "Ni", "Cu", "Zn", "Sr", "Y", "Zr"]
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    if (row['f_a'] is not None) and (row['f_spec'] is not None) and (row['f_vmag'] is not None) and (row['f_dist'] is not None) and (row['f_teff'] is not None):
      name = row['f_preferred_name']
      orbsmax = row['f_a']  #semi-major-axis of planet in AU
      spectral_type = str(row['f_spec'])[:2]
      if spectral_type == 'na':
        spectral_type = estimate_star_spect(row['f_teff'])
      app_Vmag = row['f_vmag']
      sy_dist = row['f_dist']
      inner_boundary, outer_boundary = hb_zone(spectral_type, app_Vmag, sy_dist)  #boudnaries fo habtiabel zone
      distance_from_star = (orbsmax - inner_boundary) / (outer_boundary - inner_boundary)  # normalized distance from star

      # Extract desired columns for each planet
      star_hypatia = [row['Fe'], row['Li'], row['C'], row['N'], row['O'], row['Na'], row['Mg'], row['Al'], row['Si'], row['P'], row['S'], row['K'], row['Ca'], row['Sc'], row['Ti'], row['V'], row['Cr'], row['Mn'], row['Co'], row['Ni'], row['Cu'], row['Zn'], row['Sr'], row['Y'], row['Zr']]
      predicted_composition = predict_planetary_composition(star_hypatia, distance_from_star)
      all_data[name] = [star_hypatia, predicted_composition]

run = True
while run is True:
  user_in = input("Enter the name of the planet you want to know the composition of: ")
  try:
    predicted_compositions = all_data[user_in][-1]
    print(f"Predicted Elemental Composition for {user_in}:")
    for i in range(0, len(predicted_compositions)):
      print(f"{elements[i]}: {predicted_compositions[i]}")
  except KeyError:
    print("Invalid Input")
  run = input("Would you like to continue? (y/n) ") == 'y'