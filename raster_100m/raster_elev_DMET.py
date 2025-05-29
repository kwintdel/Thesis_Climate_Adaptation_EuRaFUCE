import xarray as xr
import rasterio
import rioxarray as rxr
import matplotlib.pyplot as plt
import os
import numpy as np

# File paths
file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/elevation/merged_DMET.tif'
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/elev_DMET_new'

# Load Copernicus DSM raster
ds = rxr.open_rasterio(file_path, parse_coordinates=True, masked=True, chunks={'x': 10000, 'y': 10000})


# Function to replace "tas_" with "elev"
def modify_variable_string(input_string):
    return 'elev_DMET_' + input_string

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a NetCDF file
        print(f"Processing: {filename}")
        filename_new = modify_variable_string(filename)

        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename_new)

        # Open the NetCDF file
        city = xr.open_dataset(input_path)
        dummy_data = np.ones(shape=(len(city.y), len(city.x)))
        city["dummy_var"] = (("y", "x"), dummy_data)

        # Get the bounding box coordinates
        min_lon = city['x'].min().item() 
        min_lat = city['y'].min().item() 
        max_lon = city['x'].max().item() 
        max_lat = city['y'].max().item() 

        # Clip and interpolate the raster
        clipped = ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
        interpolated = clipped.interp_like(city)


        # Save the interpolated dataset
        interpolated.to_netcdf(output_path)
