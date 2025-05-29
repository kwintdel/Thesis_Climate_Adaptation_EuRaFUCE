import xarray as xr
from rasterio.enums import Resampling
import os

# Specify the directories
era_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA/ERA_RH'
city_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/ERA_RH_new_sep'

# Loop over all ERA5 files in the era_dir
for era5_file in os.listdir(era_dir):
    if era5_file.endswith(".nc"):
        print(f"Working on: {era5_file}")

        # Open the ERA5 file
        era5_path = os.path.join(era_dir, era5_file)
        ds = xr.open_dataset(era5_path).rio.write_crs("EPSG:4326")

        date = era5_file[8:-3]

        # Loop over all city files in the city_dir
        for city_file in os.listdir(city_dir):
            print(f"Processing city file: {city_file}")

            city_file_path = os.path.join(city_dir, city_file)
            city = xr.open_dataset(city_file_path)

            # Extract city name from the city file
            city_name = city_file[ :-3]

            # Create a directory for the city if it does not exist
            city_output_dir = os.path.join(output_dir, city_name)
            os.makedirs(city_output_dir, exist_ok=True)

            # Modify the variable string for the output file name
            output_filename = f"{city_name}_ERA5_RH_{date}_new.nc"
            output_path = os.path.join(city_output_dir, output_filename)

            # Get the bounding box from the city file
            min_lon = city['x'].min() - 0.25
            min_lat = city['y'].min() - 0.25
            max_lon = city['x'].max() + 0.25
            max_lat = city['y'].max() + 0.25

            # Select only the variables of interest (Relative Humidity)
            variables_of_interest = ["r"]  # Relative Humidity

            # Clip the dataset to the bounding box
            clipped_ds = ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat).interp(longitude=city['x'], latitude=city['y'], method="nearest")[variables_of_interest]

            # Save the selected data to a new NetCDF file
            clipped_ds.to_netcdf(output_path)

            print(f"Saved file: {output_path}")
