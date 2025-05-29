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
    return 'CORINE_perc_' + input_string

def reclassify_corine(data, mapping):
    """Reclassify CORINE land cover data to UrbClim categories."""
    reclassified = np.vectorize(mapping.get)(data, 0)  # Default to 0 if not in mapping
    return reclassified

def clip_to_city_extent(ds, city):
    """Clip ds to the extent of city without aligning x and y coordinates."""
    minx, miny, maxx, maxy = city.rio.bounds()
    ds_clipped = ds.rio.clip_box(minx, miny, maxx, maxy)
    return ds_clipped

corine_to_urbclim = {
    1: 1, 2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 10: 4, 11: 4, 34: 5, 8: 6, 9: 6, 30: 6, 31: 6, 38: 6, 39: 6,
    7: 7, 18: 7, 26: 7, 27: 7, 32: 7, 35: 7, 36: 7, 37: 7, 12: 8, 13: 8, 14: 8, 19: 8, 20: 8, 21: 8,
    15: 9, 28: 9, 29: 9, 33: 9, 16: 10, 17: 10, 22: 10, 23: 11, 25: 11, 24: 12, 40: 13, 41: 14, 42: 15, 43: 15, 44: 15
}

# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/CORINE_perc_new'

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):
        filename_new = modify_variable_string(filename)
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename_new)
        
        # Open the NetCDF file
        city = xr.open_dataset(input_path)
        
        # Clip ds to the extent of city
        ds_clipped = clip_to_city_extent(ds, city)
        
        # Extract land cover data from the first band
        land_cover_data = ds_clipped.isel(band=0)
        
        # Reclassify land cover to UrbClim categories
        land_cover_data.values = reclassify_corine(land_cover_data.values, corine_to_urbclim)
        
        # Create a weight grid to count the number of contributing pixels per 1km cell
        weight_grid = xr.ones_like(land_cover_data)
        weight_resampled = weight_grid.rio.reproject_match(city, resampling=Resampling.sum)  # Sum gives pixel count per 1km cell

        new_vars = {}
        unique_categories = set(corine_to_urbclim.values())

        for category in unique_categories:
            category_mask = (land_cover_data == category).astype(int)
            
            # Resample using sum to get the count of each category in the new 1km grid
            category_resampled = category_mask.rio.reproject_match(city, resampling=Resampling.sum)
            
            # Normalize dynamically using weight_resampled (total contributing 100m pixels per 1km pixel)
            percentage_cover = (category_resampled / weight_resampled) * 100  # Convert to percentage
            
            # Fill NaN values (where the category is absent) with 0
            percentage_cover = percentage_cover.fillna(0)  # If no category found, set to 0

            new_vars[f'LC_{category}_perc'] = percentage_cover
        
        # Create new dataset with percentage cover variables
        ds_new = xr.Dataset(new_vars)
        ds_new = ds_new.drop_vars(['band'])
        ds_new.to_netcdf(output_path)

