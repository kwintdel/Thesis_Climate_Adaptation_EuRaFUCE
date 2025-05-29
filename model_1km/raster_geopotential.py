import xarray as xr
import rasterio
import rioxarray as rxr
from rasterio.enums import Resampling
import os

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA_altitude/geopotential_ERA5.nc'
ds =xr.open_dataset(file_path)
ds['longitude'] = (ds['longitude'] + 180) % 360 - 180
ds.rio.write_crs('EPSG:4326', inplace=True)
ds = ds.rename({"longitude": "x", "latitude": "y"})



# Function to replace "tas_" with "geopot" and remove the "_UrbClim_2015_09_v1.0" part
def modify_variable_string(input_string):
    modified_string = 'ERA5_geopot_' + input_string
    return modified_string


# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/geopot_new'

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
        city = city.expand_dims(time=ds['time'])
        
        ds.interp_like(city, method='nearest').to_netcdf(output_path) #no need to resample, as the resolution of geopotential is lower than 1km





