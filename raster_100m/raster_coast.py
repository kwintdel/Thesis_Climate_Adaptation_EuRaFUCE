import xarray as xr
import rasterio
import rioxarray as rxr
import pandas as pd
import os

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/coast/proximity_coast.tif'
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True)
ds = ds.rio.reproject('EPSG:4326')
ds= ds/1000

# Function to replace "tas_" with "coast" 
def modify_variable_string(input_string):
    modified_string = 'coast_' + input_string
    return modified_string


# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/coast_new'

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
        

        min_lon=city['x'].min()
        min_lat=city['y'].min()
        max_lon=city['x'].max()
        max_lat=city['y'].max()

        ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat).interp_like(city).to_netcdf(output_path)
