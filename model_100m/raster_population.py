import xarray as xr
import rasterio
import rioxarray as rxr
import pandas as pd
import os
from dask.distributed import Client, LocalCluster
from rasterio.enums import Resampling
import numpy as np

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/population/GHS_POP_E2015_GLOBE_R2023A_54009_100_V1_0.tif'
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True, chunks={'x': 10000, 'y': 10000})


# Function to replace "tas_" with "population" 
def modify_variable_string(input_string):
    modified_string = 'population_' + input_string
    return modified_string


# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_100m/model_100m_reference'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_100m/population_new'

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
        dummy_data = np.ones(shape=(len(city.y), len(city.x)))
        city["dummy_var"] = (("y", "x"), dummy_data)
        city_reproj = city.rio.reproject('ESRI:54009')
        

        min_lon=city_reproj['x'].min()
        min_lat=city_reproj['y'].min()
        max_lon=city_reproj['x'].max()
        max_lat=city_reproj['y'].max()

        ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat).rio.reproject('EPSG:4326').interp_like(city).to_netcdf(output_path)

