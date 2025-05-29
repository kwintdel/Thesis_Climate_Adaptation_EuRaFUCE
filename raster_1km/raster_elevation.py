import xarray as xr
import rasterio
import rioxarray as rxr
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
import os
import numpy as np

# File paths
file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/elevation/copernicus_DSM_100m_new.tif'
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_1km_results'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/elev_new'

# Load Copernicus DSM raster
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True, chunks={'x': 10000, 'y': 10000})
ds /=1000

# Function to replace "tas_" with "elev"
def modify_variable_string(input_string):
    return 'elev_' + input_string

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a NetCDF file
        filename_new = modify_variable_string(filename)

        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename_new)
        # Check if the file already exists
        if os.path.exists(output_path):
            continue  # Skip this iteration if file exists

        # Open the NetCDF file
        city = xr.open_dataset(input_path)
        dummy_data = np.ones(shape=(len(city.y), len(city.x)))
        city["dummy_var"] = (("y", "x"), dummy_data)

        # Clip and interpolate the raster
        interpolated = ds.rio.reproject_match(city, resampling = Resampling.average)
        
        # Save the interpolated dataset
        interpolated.to_netcdf(output_path)
