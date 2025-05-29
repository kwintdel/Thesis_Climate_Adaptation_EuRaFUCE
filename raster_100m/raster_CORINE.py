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
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/CORINE_new'

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

        # Get the bounding box coordinates
        min_lon = city['x'].min().item()
        min_lat = city['y'].min().item()
        max_lon = city['x'].max().item()
        max_lat = city['y'].max().item()

        # Check if the raster has data within the bounding box
        #if not has_data_within_bounds(ds, min_lon, min_lat, max_lon, max_lat):
         #   print(f"No data for city: {filename}")
          #  continue  # Skip processing this city if no data is present


        # Save the resampled dataset to NetCDF
        ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat).reindex_like(city, method="nearest").to_netcdf(output_path)
