import xarray as xr
import numpy as np
from scipy.interpolate import griddata
import os

# Specify the directories
era_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA/ERA_RH'
city_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_1km_results'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_RH_interp_sep'

# Loop over all ERA5 files in the era_dir
for era5_file in os.listdir(era_dir):
    if era5_file.endswith(".nc"):
        print(f"Working on: {era5_file}")

        # Open the ERA5 file
        era5_path = os.path.join(era_dir, era5_file)
        ds = xr.open_dataset(era5_path).rio.write_crs("EPSG:4326")
        ds = ds.rename({"longitude": "x", "latitude": "y"}) #this is because the reproject match doesn't work otherwise as the city files use x and y instead of longitude and latitude
        # Select only the variables of interest (Relative Humidity)
        variables_of_interest = "r"  # Relative Humidity

        lons = ds["x"].values  # 31 km longitude array
        lats = ds["y"].values  # 31 km latitude array
        date = era5_file[8:-3]

        # Loop over all city files in the city_dir
        for city_file in os.listdir(city_dir):
            print(f"Processing city file: {city_file}")

            city_file_path = os.path.join(city_dir, city_file)
            city = xr.open_dataset(city_file_path)

            # Extract city name from the city file
            city_name = city_file[0:-3]

            # Create a directory for the city if it does not exist
            city_output_dir = os.path.join(output_dir, city_name)
            os.makedirs(city_output_dir, exist_ok=True)

            # Modify the variable string for the output file name
            output_filename = f"{city_name}_ERA5_RH_{date}_new.nc"
            output_path = os.path.join(city_output_dir, output_filename)
            # Check if the file already exists
            if os.path.exists(output_path):
                continue  # Skip this iteration if file exists

            city_lons = city["x"].values  # 1 km longitude
            city_lats = city["y"].values  # 1 km latitude

            # Find the bounding box of the city
            lon_min, lon_max = city_lons.min(), city_lons.max()
            lat_min, lat_max = city_lats.min(), city_lats.max()

            # Select only the relevant part of the 31 km dataset (reduces memory usage)
            lon_mask = (lons >= lon_min - 1) & (lons <= lon_max + 1)  # Slight buffer
            lat_mask = (lats >= lat_min - 1) & (lats <= lat_max + 1)

            subset_lons = lons[lon_mask]
            subset_lats = lats[lat_mask]
            del lon_mask
            del lat_mask
            subset_data = ds[variables_of_interest].sel(x=subset_lons, y=subset_lats).values

            # Get the number of time steps
            time_dim = subset_data.shape[0]

            # Create meshgrid of subset and city
            lon_grid, lat_grid = np.meshgrid(subset_lons, subset_lats)  # Shape: (lat, lon)
            city_lon_grid, city_lat_grid = np.meshgrid(city_lons, city_lats)  # (city_lat, city_lon)
            del subset_lons
            del subset_lats
            del city_lons
            del city_lats

            # Flatten the original dataset for interpolation
            orig_points = np.column_stack([lon_grid.ravel(), lat_grid.ravel()])  # Shape: (lat*lon, 2)
            del lon_grid
            del lat_grid

            # Prepare an empty array for results
            interpolated_values = np.empty((time_dim, *city_lon_grid.shape))  # (time, city_lat, city_lon)

            # Loop efficiently over time steps
            for t in range(time_dim):

                orig_values = subset_data[t].ravel()  # Flatten for interpolation

                # Perform linear interpolation for this time step
                interpolated_values[t] = griddata(
                    orig_points, orig_values, (city_lon_grid, city_lat_grid), method="linear"
                )
            del subset_data
            del orig_values
            del orig_points
            del city_lon_grid
            del city_lat_grid

            # Store the interpolated data in the city dataset
            city[variables_of_interest] = (("time", "y", "x"), interpolated_values)

            # Keep original time dimension
            city["time"] = ds["time"]

            # Save the selected data to a new NetCDF file
            city.to_netcdf(output_path)

            print(f"Saved file: {output_path}")
