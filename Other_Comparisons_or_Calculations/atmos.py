import numpy as np

# Load transmission spectra data (GJ436 b)
wavelengths = np.array([1.155, 1.174, 1.193, 1.211, 1.23, 1.249, 1.268, 1.289, 1.306, 1.324, 
                        1.343, 1.362, 1.381, 1.4, 1.419, 1.438, 1.456, 1.475, 1.494, 1.513, 
                        1.532, 1.551, 1.57, 1.588, 1.607, 1.626, 1.645])
rp_rs_squared = np.array([0.006994, 0.006924, 0.006872, 0.006968, 0.007046, 0.007036, 0.006967, 
                          0.006979, 0.007043, 0.006989, 0.007046, 0.007057, 0.007006, 0.007036, 
                          0.007072, 0.00703, 0.007044, 0.006948, 0.007008, 0.007057, 0.007022, 
                          0.007018, 0.00701, 0.006959, 0.006994, 0.006984, 0.006984])
uncertainty = np.array([0.00005, 0.00004, 0.000057, 0.000039, 0.000038, 0.000039, 0.000035, 
                        0.000035, 0.000038, 0.000038, 0.000042, 0.000037, 0.000037, 0.00005, 
                        0.000046, 0.000042, 0.000042, 0.000039, 0.000039, 0.00004, 0.000044, 
                        0.00004, 0.000037, 0.00004, 0.000044, 0.000044, 0.000059])

# Identify absorption features
# For demonstration, let's assume a simple method of finding peaks in the spectrum
peaks_indices = np.where(rp_rs_squared > np.mean(rp_rs_squared))[0]
absorption_features = wavelengths[peaks_indices]

# Match absorption features to known molecules
# For demonstration, let's assume hypothetical matching based on approximate wavelengths
matched_molecules = []
for feature in absorption_features:
    if 1.1 < feature < 1.2:
        matched_molecules.append("Water Vapor")
    elif 3.5 < feature < 8:
        matched_molecules.append("Methane")
    # Add more conditions for additional molecules

# Output composition estimate
print("Estimated Atmospheric Composition:")
for i, molecule in enumerate(matched_molecules):
    print(f"Feature {i+1}: {molecule}")
