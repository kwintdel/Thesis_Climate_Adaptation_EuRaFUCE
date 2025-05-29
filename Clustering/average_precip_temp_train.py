import numpy as np
import pandas as pd
import dask.dataframe as dd
import glob

# Define the file path pattern for all the relevant CSV files
file_path_pattern = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER*_cities.csv'

# Use glob to find all matching file paths
file_paths = glob.glob(file_path_pattern)

# Load and concatenate all files into a single Dask DataFrame
cities = dd.concat([dd.read_csv(file, blocksize=50e6) for file in file_paths], axis=0)
# Select the relevant columns
cities_selected = cities[['city', 'PRECIP', 'T_TARGET']]

# Compute the mean of 'PRECIP' and 'T_2M_CORR' for each city
averaged_data = cities_selected.groupby('city')[['PRECIP', 'T_TARGET']].mean().reset_index()
averaged_data['city'] = averaged_data['city'].map(lambda x: x.split('_')[0], meta=('city', 'str'))

# Rename the columns for clarity
averaged_data = averaged_data.rename(columns={
    'PRECIP': 'Average_PRECIP',
    'T_TARGET': 'Average_T_TARGET',
    'city': 'City'
})

# Save the result to a CSV file
output_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/average_precip_temp_train.csv'
averaged_data.compute().to_csv(output_path, index=False)

print(f"File saved to {output_path}")
