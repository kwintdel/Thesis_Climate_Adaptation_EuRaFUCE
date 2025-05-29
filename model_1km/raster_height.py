import xarray as xr
import rasterio
import rioxarray as rxr
from rasterio.enums import Resampling
import pandas as pd
import os

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/height/GHS_BUILT_H_AGBH_E2018_GLOBE_R2023A_54009_100_V1_0.tif'
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True)
ds = ds.rio.reproject('EPSG:4326')


# Function to replace "tas_" with "height"
def modify_variable_string(input_string):
    modified_string = 'height_' + input_string
    return modified_string


# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/height_new'

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)


# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a netCDF file
        filename_new= modify_variable_string(filename)

        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename_new)
  
        # Open the netCDF file
        city = xr.open_dataset(input_path)

        ds.rio.reproject_match(city, resampling = Resampling.average).to_netcdf(output_path)

