import xarray as xr
import pandas as pd
import os
import numpy as np
from collections import Counter

# Function to replace "tas_" with "coast" 
def modify_variable_string(input_string):
    modified_string = 'char_' + input_string
    return modified_string

def calc_stats(input_path):
    # Mapping of CORINE classes to UrbClim classes
    corine_to_urbclim = {
        1: 'Urban',
        2: 'Sub-urban',
        3: 'Industrial', 4: 'Industrial', 5: 'Industrial', 6: 'Industrial',
        10: 'Urban green', 11: 'Urban green',
        34: 'Snow/Ice',
        8: 'Bare soil', 9: 'Bare soil', 30: 'Bare soil', 31: 'Bare soil', 38: 'Bare soil', 39: 'Bare soil',
        7: 'Grassland', 18: 'Grassland', 26: 'Grassland', 27: 'Grassland', 32: 'Grassland', 35: 'Grassland', 36: 'Grassland', 37: 'Grassland',
        12: 'Cropland', 13: 'Cropland', 14: 'Cropland', 19: 'Cropland', 20: 'Cropland', 21: 'Cropland',
        15: 'Shrubland', 28: 'Shrubland', 29: 'Shrubland', 33: 'Shrubland',
        16: 'Woodland', 17: 'Woodland', 22: 'Woodland',
        23: 'Broadleaf trees', 25: 'Broadleaf trees',
        24: 'Needleleaf trees',
        40: 'Rivers',
        41: 'Inland water bodies',
        42: 'Sea', 43: 'Sea', 44: 'Sea'
    }

    # Open the .nc file and extract the data array
    overall_data = xr.open_dataset(input_path)
    data_array = overall_data["__xarray_dataarray_variable__"].values.flatten()

    # Map CORINE classes to UrbClim classes
    urbclim_classes = [corine_to_urbclim.get(value, 'Unknown') for value in data_array]

    # Count occurrences of each UrbClim class
    class_counts = Counter(urbclim_classes)

    # Ensure all categories from corine_to_urbclim are present, setting missing categories to 0
    all_categories = sorted(set(corine_to_urbclim.values()))
    percentages = {category: class_counts.get(category, 0) for category in all_categories}

    # Calculate total pixel count
    total_pixels = sum(percentages.values())
    if total_pixels > 0:
        percentages = {category: count / total_pixels for category, count in percentages.items()}

    # Convert to DataFrame
    percentages_df = pd.DataFrame(list(percentages.items()), columns=['UrbClim Class', 'Percentage'])
    percentages_df = percentages_df.sort_values(by='UrbClim Class')  # Sort alphabetically

    return percentages_df

# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
CORINE_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/CORINE_new'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/CORINE_stats'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(CORINE_directory):
    if filename.endswith('.nc'):  # Check if the file is a netCDF file
        filename_new = modify_variable_string(filename)

        CORINE_path = os.path.join(CORINE_directory, filename)
        output_path = os.path.join(output_directory, filename_new)

        # Calculate statistics and save to CSV
        CORINE_df = calc_stats(CORINE_path)
        CORINE_df.columns = ['Variable', 'median']
        print(CORINE_df)

        CORINE_df.to_csv(output_path, index=False)
