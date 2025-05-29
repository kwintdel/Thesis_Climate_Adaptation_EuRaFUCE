import xarray as xr
from rasterio.enums import Resampling
import os

# Specify the directories
era_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA/ERA_RH'
city_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/rasters_1km_reference'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/ERA_RH_new_sep'

# Loop over all ERA5 files in the era_dir
for era5_file in os.listdir(era_dir):
    if era5_file.endswith(".nc"):
        print(f"Working on: {era5_file}")

        # Open the ERA5 file
        era5_path = os.path.join(era_dir, era5_file)
        ds = xr.open_dataset(era5_path).rio.write_crs("EPSG:4326")
        ds = ds.rename({"longitude": "x", "latitude": "y"}) #this is because the reproject match doesn't work otherwise as the city files use x and y instead of longitude and latitude

        date = era5_file[8:-3]

        # Loop over all city files in the city_dir
        for city_file in os.listdir(city_dir):
            print(f"Processing city file: {city_file}")

            city_file_path = os.path.join(city_dir, city_file)
            city = xr.open_dataset(city_file_path)

            # Extract city name from the city file
            city_name = city_file[4:-3]

            # Create a directory for the city if it does not exist
            city_output_dir = os.path.join(output_dir, city_name)
            os.makedirs(city_output_dir, exist_ok=True)

            # Modify the variable string for the output file name
            output_filename = f"{city_name}_ERA5_RH_{date}_new.nc"
            output_path = os.path.join(city_output_dir, output_filename)

            # Select only the variables of interest (Relative Humidity)
            variables_of_interest = ["r"]  # Relative Humidity

            # Clip the dataset to the bounding box of the city
            clipped_ds = ds.rio.reproject_match(city, resampling=Resampling.average)[variables_of_interest]

            # Save the selected data to a new NetCDF file
            clipped_ds.to_netcdf(output_path)

            print(f"Saved file: {output_path}")
