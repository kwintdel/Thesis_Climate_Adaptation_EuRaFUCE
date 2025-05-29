import os
import xarray as xr
import numpy as np
import rioxarray
from rasterio.enums import Resampling

# Define the directories
input_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/Urbclim_data/Urbclim_non_projected'
reference_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_base_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/Urbclim_separate'

# Ensure the output base directory exists
os.makedirs(output_base_dir, exist_ok=True)

# Get the reference city names
reference_files = os.listdir(reference_dir)
reference_cities = {
    file_name[4:-3]: os.path.join(reference_dir, file_name)
    for file_name in reference_files if file_name.endswith('.nc')
}


# Process each file in the input directory
input_files = os.listdir(input_dir)
for input_file in input_files:
    if input_file.endswith('.nc'):
        # Extract the city name and file-specific name
        city_name = input_file[4:-24]
        filename_new = input_file[4:-8]

        # Open the input 100m resolution file
        input_path = os.path.join(input_dir, input_file)
        with xr.open_dataset(input_path) as input_data:

            # Check if the city has a reference file
            if city_name not in reference_cities:
                print(f"No reference file for city: {city_name}")
                continue
            # Remove latitude and longitude coordinates if present
            input_data = input_data.drop_vars(["latitude", "longitude"], errors="ignore")
            
            input_data = input_data.rio.write_crs('EPSG:3035')
            # Open the reference 1km resolution file to align the grid
            ref_path = reference_cities[city_name]
            with xr.open_dataset(ref_path) as ref_data:

                # Reproject the input data to match the reference grid
                resampled_data = input_data.rio.reproject_match(ref_data, resampling = Resampling.average)

                # Define the output directory and file path
                city_output_dir = os.path.join(output_base_dir, city_name)
                os.makedirs(city_output_dir, exist_ok=True)
                output_path = os.path.join(city_output_dir, f"{filename_new}_new.nc")

                # Save the resampled data to the new file
                resampled_data.to_netcdf(output_path)
                print(f"Processed and saved: {output_path}")

print("Processing completed.")
