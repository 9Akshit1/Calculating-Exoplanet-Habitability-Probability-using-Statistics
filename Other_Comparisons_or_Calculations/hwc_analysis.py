import pandas as pd
import math
import csv
import os


def calculate_albedo(density, radius):
  terrestrial_density_range = (3.0, 6.0)
  super_earth_density_range = (6.1, 11.0)
  ice_density_range = (0.9, 2.9)
  gas_density_range = (0.8, 2.0)
  puffy_gas_density_range = (0.04, 0.79)

  albedo_values = {
      "Terrestrial": 0.3,
      "Super Earth": 0.25,
      "Ice": 0.45,
      "Gas": 0.5,
      "Puffy Gas": 0.4,
      "Unknown": 0.4
  }

  planet_type = ""

  if terrestrial_density_range[0] <= density <= terrestrial_density_range[1]:
    planet_type = "Terrestrial"
  elif super_earth_density_range[0] <= density <= super_earth_density_range[1]:
    planet_type = "Super Earth"
  elif ice_density_range[0] <= density <= ice_density_range[1]:
    planet_type = "Ice"
  elif gas_density_range[0] <= density <= gas_density_range[1]:
    planet_type = "Gas"
  elif puffy_gas_density_range[0] <= density <= puffy_gas_density_range[1]:
    planet_type = "Puffy Gas"
  else:
    planet_type = "Unknown"

  estimated_albedo = albedo_values[planet_type]

  return estimated_albedo


def estimatePlanetType(density, temp, Emass):
  terrestrial_density_range = [3.0, 6.0]
  super_earth_density_range = [6.1, 11.0]
  ice_density_range = [0.9, 1.9]
  gas_density_range = [0.8, 2.0]
  puffy_gas_density_range = [0.04, 0.79]

  planet_type = ""

  if terrestrial_density_range[0] <= density <= terrestrial_density_range[1]:
    if Emass < 350:
      planet_type = "Terrestrial"
    else:
      planet_type = "Gas"
  elif super_earth_density_range[0] <= density <= super_earth_density_range[1]:
    if Emass < 350:
      planet_type = "Super Earth"
    else:
      planet_type = "Gas"
  elif ice_density_range[0] <= density <= ice_density_range[1]:
    planet_type = "Ice"
  elif gas_density_range[0] <= density <= gas_density_range[1]:
    planet_type = "Gas"
  elif puffy_gas_density_range[0] <= density <= puffy_gas_density_range[1]:
    planet_type = "Puffy Gas"
  else:
    planet_type = "Unknown"

  return planet_type



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


def is_within_habitable_zone(orbsmaxm, spectral_type, app_mag, sy_dist):

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
      "B8": -1.255,  #estimated
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
      "F7": -0.18,  #estimated
      "F8": -0.21,
      "F9": -0.24,  #estimated
      "G0": -0.27,
      "G1": -0.305,  #estimated
      "G2": -0.34,
      "G3": -0.38,  #estimated
      "G4": -0.42,
      "G5": -0.46,  #estimated
      "G6": -0.50,
      "G7": -0.535,  #estimated
      "G8": -0.57,
      "G9": -0.605,  #estimated
      "K0": -0.64,
      "K1": -0.675,  #estimated
      "K2": -0.71,
      "K3": -0.74,  #estimated
      "K4": -0.77,
      "K5": -0.81,  #estimated
      "K6": -0.85,
      "K7": -0.89,  #estimated
      "K8": -0.97,
      "K9": -1.24,  #estimated
      "M0": -1.51,
      "M1": -2.395,  #estimated
      "M2": -3.28,
      "M3": -3.62,  #estimated
      "M4": -3.96,
      "M5": -4.26,
      "M6": -4.63,  #estimated
      "M7": -5.16,  #estimated
      "M8": -5.52,  #estimated
  }

  abs_mag = app_mag - 5 * math.log10(
      sy_dist / 10)  #calculate absolute magnitude
  bol_mag = abs_mag + BC_constants[spectral_type]
  rel_lumin = 10**((bol_mag - 4.72) / (-2.5))

  r_i = math.sqrt(rel_lumin / 1.1)
  r_o = math.sqrt(rel_lumin / 0.53)

  return r_i, r_o


def calculate_density_gravity(mass_earth, radius_earth):
  radius_cm = radius_earth * 6371 * 10**5
  mass_g = mass_earth * 5.972 * 10**27
  volume = (4 / 3) * math.pi * radius_cm**3
  density_g_cm3 = mass_g / volume

  G = 6.674 * (10**-11)  # Gravitational constant in m^3/kg*s^2
  surface_gravity = ((G * (mass_earth * 5.972 * 10**24)) /
                     ((radius_earth * 6371 * 10**3)**2))

  return density_g_cm3, surface_gravity


def calculate_RHP_values(file_path):
  habitable_probs_vals = []
  habitable_probs_names = []
  list_of_planets = []
  earth_like = []
  new_dataset = []

  try:
    df = pd.read_csv(file_path)   
    new_dataset.append(df.columns.tolist())  
    filtered_columns = [   
        "P_NAME", "S_NAME", "P_YEAR", "P_PERIOD",
        "P_DISTANCE", "P_RADIUS", "P_MASS", "P_ECCENTRICITY", "P_FLUX",
        "P_TEMP_EQUIL", 'P_TEMP_SURF', 'P_INCLINATION', 'P_DENSITY', 'P_GRAVITY', "S_TYPE", "S_TEMPERATURE",
        "S_RADIUS", "S_MASS", "S_METALLICITY", "S_LOG_G", "S_DISTANCE",
        "S_MAG", 'S_HZ_CON_MIN', 'S_HZ_CON_MAX',"P_ESI"
    ]
    filtered_df = df[filtered_columns]
    columns = filtered_df.columns.tolist()
    print("Filtered column names:")
    print(columns)
    print("Filtered rows:")
    for index, row in filtered_df.iterrows():
      if not math.isnan(row['P_MASS']) and not math.isnan(
          row['P_TEMP_EQUIL']) and not math.isnan(
              row['P_FLUX']) and not math.isnan(row['S_TEMPERATURE']):
        new_dataset.append(row)
        st_name = row['S_NAME']
        #sy_snum = row['sy_snum']
        #sy_pnum = row['sy_pnum']
        disc_year = row['P_YEAR']
        st_rad = row['S_RADIUS'] * 696340  #696340km is Suns' radius

        #others: P_OMEGA, S_LUMINOSITY, P_ESCAPE, P_GRAVITY, P_DENSITY, P_TEMP_SURF, P_TYPE, S_HZ_(OPT, CON, CON0, CON1)_(MIN, MAX), S_SNOW_LINE, S_ABIO_ZONE, S_TIDAL_LOCK, P_HABITABLE, P_ESI
        pl_name = row['P_NAME']
        pl_Erad = row['P_RADIUS']
        pl_Emass = row['P_MASS']
        eq_temp = row['P_TEMP_EQUIL']
        pl_insol = row[
            'P_FLUX'] * 1360  #At a distance of 1 a.u., the intensity of the incoming solar flux is ~1360 W/m2 fro earth from the sun
        pl_orbper = row['P_PERIOD']
        pl_orbsmax = row['P_DISTANCE']  #mean distance fro mstar
        pl_orbeccen = row['P_ECCENTRICITY']
        pl_inclin = row['P_INCLINATION']
        #pl_obliq = row['pl_trueobliq']  #axial tilt basically
        pl_esi = row['P_ESI'] * 100  #new
        #pl_surf_temp = row['P_TEMP_SURF']  #new

        st_teff = row['S_TEMPERATURE']
        st_spectype_list = str(row['S_TYPE']).split()
        st_spectype = "".join(str(element) for element in st_spectype_list)
        st_mass = row['S_MASS']
        st_rad = row['S_RADIUS']
        st_met = row["S_METALLICITY"]
        #st_metratio = row["st_metratio"]
        st_log_gravity = row["S_LOG_G"]

        sy_vmag = row['S_MAG']
        sy_dist = row['S_DISTANCE']

        pl_density, pl_gravity = calculate_density_gravity(pl_Emass, pl_Erad)
        #pl_density, pl_gravity = row['P_DENSITY'], row['P_GRAVITY']   #new
 
        pl_albedo = calculate_albedo(pl_density, pl_Erad)
        pl_type = estimatePlanetType(pl_density, eq_temp, pl_Emass)

        abs_solar_flux = 1 - pl_albedo
        if len(st_spectype) >= 2:
            if st_spectype[:2] == 'na':
                star_spect = estimate_star_spect(st_teff)
            else:
                star_spect = st_spectype[:2]
        else:
          star_spect = estimate_star_spect(st_teff)

        #HB_r_i, HB_r_o = is_within_habitable_zone(float(pl_orbsmax), str(star_spect), float(sy_vmag), float(sy_dist))
        HB_r_i, HB_r_o = row['S_HZ_CON_MIN'], row['S_HZ_CON_MAX']  #new

        ideal_ranges = {
            "eq_temp": (213, 313),  #around -60C to 40C
            "abs_solar_flux": (0.8, 0.6),
            "star_spectral": (["M", "G", "K"], ["F"]),
            "planet_type": (["Terrestrial", "Super Earth"], ["Ice"]),
            "planet_gravity":
            (4.9, 29.4
             ),  #based of our gravity so there coudl eb error here         
            "close_to_HB_zone": (HB_r_i, HB_r_o)
        }

        weights = {
            "eq_temp":
            0.3,  #very important
            "abs_solar_flux": 0.15,  #kinda important, some species quite resistant to radiation though, like tardigrades 
            "star_spectral":
            0.1,  #lifespan of star mattersi n long term and also it grows more dangerous
            "planet_type": 0.25,
            "planet_gravity":
            0.05,  #low cuz its jsut gravity
            "close_to_HB_zone": 0.15 #little important
        }

        actual_values = {
            "eq_temp": eq_temp,
            "abs_solar_flux": abs_solar_flux,
            "star_spectral": star_spect,
            "planet_type": pl_type,
            "planet_gravity": pl_gravity,
            "close_to_HB_zone": pl_orbsmax
        }

        probability = 0

        for param, (ideal_min, ideal_max) in ideal_ranges.items():
          match param:
            case 'star_spectral':
              if actual_values[param][0] in ideal_ranges[param][0]:
                probability += 100 * weights[param]
              elif actual_values[param][0] in ideal_ranges[param][1]:
                probability += 50 * weights[param]
            case 'planet_type':
              if actual_values[param] in ideal_min:
                probability += 100 * weights[param]
              elif actual_values[param] in ideal_max:
                probability += 20 * weights[param]
            case _:
              avg_range = (ideal_min + ideal_max) / 2
              transform_const = -0.005 if (
                  param == "eq_temp" or param == "planet_gravity") else (
                      -100 if param == "abs_solar_flux" else -4)

              perc = 100 * math.e**(
                  transform_const * (actual_values[param] - avg_range)**2
              )

              print(param + ":", perc)

              probability += perc * weights[param]

        new_row = [
            pl_name, st_name, disc_year, pl_orbper,
            pl_orbsmax, pl_Erad, pl_Emass, pl_orbeccen, pl_insol, eq_temp,
            pl_inclin, pl_density, pl_gravity, pl_albedo,
            abs_solar_flux, star_spect, st_teff, st_rad, st_mass, st_met,
            st_log_gravity, HB_r_i, HB_r_o, sy_dist, sy_vmag,
            probability, pl_esi
        ]

        file_path = os.path.join('data_folder_esi', st_name + '.csv')
        if os.path.exists(file_path):
          pass
        else:
          with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "pl_name", "st_name", "disc_year",
                "pl_orbper", "pl_orbsmax", "pl_Erad", "pl_Emass",
                "pl_orbeccen", "pl_insol", "eq_temp", "pl_inclin",
                "pl_density", "pl_gravity", "pl_albedo", "abs_solar_flux",
                "star_spect", "st_teff", "st_rad", "st_mass", "st_met", "st_log_gravity", "HB_r_i", "HB_r_o", "sy_dist",
                "sy_vmag", "Probability", "ESI"
            ])  #titles
            writer.writerow(new_row)

        if str(probability) != 'nan':
          print(row['P_NAME'], "-", probability, "RHP")
          if (0.6 <= pl_Erad <= 1.4) and (0.6 <= pl_Emass <= 1.4) and (
              0.2 <= pl_albedo <= 0.4) and (star_spect[0]
                                            in ['M', 'K', 'G', 'F']):
            earth_like.append([
                pl_name, pl_orbper, pl_orbsmax, pl_Erad, pl_Emass, pl_orbeccen,
                pl_insol, eq_temp, pl_inclin, pl_albedo, star_spect,
                st_teff, st_rad, st_mass, probability, pl_esi
            ])
          list_of_planets.append([pl_name, probability, pl_esi])
          habitable_probs_names.append(pl_name)
          habitable_probs_vals.append(probability)
          print("\n")

  except FileNotFoundError:
    print("File not found:", file_path)
  except Exception as e:
    print("An error occurred while reading the CSV file:", e)

  highest_prob = max(habitable_probs_vals)
  lowest_prob = min(habitable_probs_vals)

  print("\nHighest Prob:",
        habitable_probs_names[habitable_probs_vals.index(highest_prob)], "-",
        highest_prob, "RHP")
  print("Lowest Prob:",
        habitable_probs_names[habitable_probs_vals.index(lowest_prob)], "-",
        lowest_prob, "RHP\n")

  sorted_list = sorted(list_of_planets, key=lambda x: x[1], reverse=True)
  #print(sorted_list)
  csv_file_name = 'sorted_data_esi.csv'
  with open(csv_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["P_NAME", "Probability", "ESI"])  # Header row
    writer.writerows(sorted_list)

  #earth-liek planets csv file
  csv_file_name = os.path.join('data_folder_esi', 'earth_like_esi.csv')
  with open(csv_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'pl_name', 'pl_orbper', 'pl_orbsmax', 'pl_Erad', 'pl_Emass',
        'pl_orbeccen', 'pl_insol', 'eq_temp', 'pl_inclin',
        'pl_albedo', 'star_spect', 'st_teff', 'st_rad', 'st_mass',
        'Probability', 'ESI'
    ])  # Header row
    writer.writerows(earth_like)


file_path = "hwc (1).csv"  
calculate_RHP_values(file_path)
