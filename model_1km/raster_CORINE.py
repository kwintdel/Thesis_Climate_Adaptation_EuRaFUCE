import xarray as xr
import rioxarray as rxr
from rasterio.enums import Resampling  # Correct import for Resampling
import os
import numpy as np

# Load CORINE raster
file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/CORINE/corine_new.tif'
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True, chunks={'x': 10000, 'y': 10000})

# Function to replace "tas_" with "CORINE_"
def modify_variable_string(input_string):
    return 'CORINE_' + input_string

# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/CORINE_new'

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)


# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a netCDF file
        filename_new = modify_variable_string(filename)

        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename_new)

        # Check if the file already exists
        #if os.path.exists(output_path):
        #    continue  # Skip this iteration if file exists

        # Open the NetCDF file
        city = xr.open_dataset(input_path)
        dummy_data = np.ones(shape=(len(city.y), len(city.x)))
        city["dummy_var"] = (("y", "x"), dummy_data)

        # Save the resampled dataset to NetCDF
        ds.rio.reproject_match(city, resampling = Resampling.mode).to_netcdf(output_path)
