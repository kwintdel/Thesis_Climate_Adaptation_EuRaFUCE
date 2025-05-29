import numpy as np
import pandas as pd
import xarray as xr
import os
import re
import rioxarray as rxr


#load bounding box data
data = pd.read_csv("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_data/GHSL_cities_enclosedby_EU_manuallyandauto.csv", header=[0, 1], index_col=0)

#load reference raster
raster_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/height/GHS_BUILT_H_AGBH_E2018_GLOBE_R2023A_54009_100_V1_0.tif'
raster = rxr.open_rasterio(raster_path, parse_coordinates=True, masked=True).rio.reproject('EPSG:4326')

# Create a directory to store the .nc files
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
reference_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/Urbclim_data/UrbClim_reference/'
os.makedirs(output_dir, exist_ok=True)

# List all files in the reference directory and extract the city names
existing_city_files = os.listdir(reference_dir)
existing_cities = set()

# Extract CITYNAME from filenames in the format 'tas_CITYNAME_UrbClim_2015_01_v1.0.nc'
for file_name in existing_city_files:
    match = re.match(r'tas_(.+?)_UrbClim_2015_01_v1.0.nc', file_name)
    if match:
        existing_cities.add(match.group(1))

# Iterate through each city in the DataFrame
for _, row in data.iterrows():
    city_name = row['UC_NM_MN'].values[0].replace('/', '_')
    
    if city_name in existing_cities:
        print(f"Skipping {city_name} - file already exists.")
        continue
    
    # Extract bounding box coordinates
    lat_min, lon_min = row['BBX_LATMN'].values[0], row['BBX_LONMN'].values[0]
    lat_max, lon_max = row['BBX_LATMX'].values[0], row['BBX_LONMX'].values[0]

    # Create a .nc file for each city
    nc_file_path = os.path.join(output_dir, f"{city_name}.nc")

    # Clip the raster to the bounding box and Select only the x and y coordinates, dropping all other dimensions and metadata
    clipped_raster_xy = raster.rio.clip_box(minx=lon_min, miny=lat_min, maxx=lon_max, maxy=lat_max)
    clipped_raster_xy = clipped_raster_xy.sel(band=1).squeeze(drop=True)
    clipped_raster_xy.attrs = {}  # Clear metadata

    # Create a new dataset without __xarray_dataarray_variable__ and with the desired attributes
    clipped_raster_ds = xr.Dataset({
        'spatial_ref': clipped_raster_xy['spatial_ref'],  # Keep spatial reference
    }, coords={
        'x': clipped_raster_xy['x'],
        'y': clipped_raster_xy['y']
    })

    clipped_raster_ds.to_netcdf(nc_file_path)

