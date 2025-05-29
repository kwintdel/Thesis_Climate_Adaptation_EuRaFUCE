import pandas as pd
import glob
import numpy as np
import xarray as xr

# Define the folder paths
stats_folder = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/city_stats/'
rasters_folder = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results/'

# Find all stats .nc files in the city stats folder
stats_file_paths = glob.glob(f"{stats_folder}/char_*.nc")

# Initialize an empty list to store processed data
processed_data = []

# Loop through each stats file
for file in stats_file_paths:
    # Read the file as a CSV
    df = pd.read_csv(file)

    # Extract the city name from the file name
    city_name = file.split('/')[-1].replace('char_', '').replace('.nc', '')

    # Select rows for the required variables
    required_vars = ['AHF', 'PRECIP', 'T_TARGET', 'ELEV', 'COAST']
    filtered_df = df[df['Variable'].isin(required_vars)]

    # Create a dictionary to store the city data
    city_data = {'City': city_name}

    # Extract the average values and perform COAST correction
    for _, row in filtered_df.iterrows():
        var_name = row['Variable']
        avg_value = float(row['mean'])  # Extract the mean value
        if var_name == 'COAST':
            # Perform log10(COAST * 1000) correction
            avg_value = np.log10(avg_value * 1000)
        city_data[var_name] = avg_value

    # Locate the corresponding raster file for the city
    raster_file = f"{rasters_folder}/{city_name}.nc"

    # Extract latitude and longitude from the raster file
    try:
        ds = xr.open_dataset(raster_file)
        city_data['Latitude'] = ds.y.mean().item()
        city_data['Longitude'] = ds.x.mean().item()
    except FileNotFoundError:
        print(f"Raster file not found for city: {city_name}")
        city_data['Latitude'] = None
        city_data['Longitude'] = None

    # Append the city data to the list
    processed_data.append(city_data)

# Convert the processed data into a DataFrame
final_df = pd.DataFrame(processed_data)

# Ensure columns are in the desired order
final_df = final_df[['City', 'ELEV', 'T_TARGET', 'PRECIP', 'COAST', 'AHF', 'Latitude', 'Longitude']]

# Save the final DataFrame to a CSV file
output_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/new_combined.csv'
final_df.to_csv(output_path, index=False)

print(f"Combined file saved to {output_path}")
