import numpy as np
import pandas as pd
import xarray as xr
import os
import re
import rioxarray as rxr

#load reference raster this time with 1km resolution instead of 100m
raster_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/height/GHS_BUILT_H_AGBH_E2018_GLOBE_R2023A_54009_100_V1_0.tif'
raster = rxr.open_rasterio(raster_path, parse_coordinates=True, masked=True)

# Create a directory to store the .nc files
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_100m/model_100m_reference'
input_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/Urbclim_data/UrbClim_reference/'
os.makedirs(output_dir, exist_ok=True)

#for file_name in existing_city_files:
 #   if file_name.endswith('.nc'):
  #      city_name = file_name[4:-24]  # Extract city name using slicing
   #     existing_cities.add(city_name)

def modify_variable_string(input_string):
    city_name = input_string[4:-24]
    modified_string = 'm100_'+ city_name + '.nc'
    return modified_string

# Iterate through each city in the DataFrame
for filename in os.listdir(input_dir):   
    if  filename.endswith('.nc'):
        filename_new= modify_variable_string(filename)

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename_new)

        # Open the netCDF file
        city = xr.open_dataset(input_path).rio.write_crs('EPSG:4326').rio.reproject("ESRI:54009")

        min_lon=city['x'].min()
        min_lat=city['y'].min()
        max_lon=city['x'].max()
        max_lat=city['y'].max()

        # Clip the raster to the bounding box and Select only the x and y coordinates, dropping all other dimensions and metadata
        clipped_raster_xy = raster.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
        clipped_raster_xy = clipped_raster_xy.sel(band=1).squeeze(drop=True).rio.reproject('EPSG:4326')
        clipped_raster_xy.attrs = {}  # Clear metadata

        # Create a new dataset without __xarray_dataarray_variable__ and with the desired attributes
        clipped_raster_ds = xr.Dataset({
            'spatial_ref': clipped_raster_xy['spatial_ref'],  # Keep spatial reference
        }, coords={
            'x': clipped_raster_xy['x'],
            'y': clipped_raster_xy['y']
        })

        clipped_raster_ds.to_netcdf(output_path)
    print(f"{filename_new} done")

