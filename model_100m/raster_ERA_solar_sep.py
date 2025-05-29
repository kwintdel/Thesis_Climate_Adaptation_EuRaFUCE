import xarray as xr
import numpy as np
import rasterio as rio
import rioxarray as rxr
from rasterio.enums import Resampling
import os
import ephem
import pandas as pd

# Specify the directories
era_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA'
city_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_100m/model_100m_reference'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_100m/ERA_solar_new_sep'

# Function to calculate solar position
def get_solar_position(latitude, longitude, datetime_obj):
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.date = datetime_obj
    sun = ephem.Sun()
    sun.compute(observer)

    # Declination in degrees
    declination_degrees = float(sun.dec) * (180 / ephem.pi)

    # Solar elevation in degrees
    elevation_degrees = float(sun.alt) * (180 / ephem.pi)

    return elevation_degrees, declination_degrees

# Function to replace filename
def modify_variable_string(input_string):
    return 'ERA5_solar_date_' + input_string

# Loop over all ERA5 files in the era_dir
for era5_file in os.listdir(era_dir):
    if era5_file.endswith(".nc"):

        month = era5_file[10:12]  # Extract 'mm' from 'ERA_yyyy_mm.nc'
        if month not in ["06", "07", "08"]:
            continue  # Skip this file if it's not June, July, or August
        
        print(f"Working on: {era5_file}")

        # Define the full path to the ERA5 file
        era5_path = os.path.join(era_dir, era5_file)
        ds = xr.open_dataset(era5_path).rio.write_crs("EPSG:4326")

        date = era5_file[5:-3]
        # Loop over all city files in the city_dir
        for city_file in os.listdir(city_dir):

            
            print(f"Processing city file: {city_file}")
            city_file_path = os.path.join(city_dir, city_file)
            city = xr.open_dataset(city_file_path)

            # Extract city name from the city file 
            city_name = city_file[ :-3]

            # Create the output directory for the city if it doesn't exist
            city_output_dir = os.path.join(output_dir, city_name)
            os.makedirs(city_output_dir, exist_ok=True)

            # Modify the variable string for the output file name
            output_filename = f"{city_name}_ERA5_solar_{date}_new.nc"
            output_path = os.path.join(city_output_dir, output_filename)

            # Check if the file already exists
            if os.path.exists(output_path):
                continue  # Skip this iteration if file exists

            # Get the bounding box from the city file
            min_lon = city['x'].min() - 0.25
            min_lat = city['y'].min() - 0.25
            max_lon = city['x'].max() + 0.25
            max_lat = city['y'].max() + 0.25

            # Select only the variables of interest
            variables_of_interest = ["t2m", "blh", "sp", "tcc", "tp", "cape", "ssr", "ws"]

            # Clip the dataset to the bounding box
            clipped_ds = ds.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat).interp(longitude=city['x'], latitude=city['y'], method="nearest")

            # Calculate wind speed and convert tp units
            clipped_ds["ws"] = np.sqrt(clipped_ds["v10"] ** 2 + clipped_ds["u10"] ** 2)
            clipped_ds["tp"] = clipped_ds["tp"] * 1000  # Convert tp to mm/h

            # Calculate midpoint latitude and longitude
            mid_latitude = city['y'].mean().item()
            mid_longitude = city['x'].mean().item()

            # Loop over all time steps and calculate the solar position
            solar_elevations = []
            declinations = []

            for time in clipped_ds['time']:
                # Convert the time to a datetime object
                datetime_obj = pd.to_datetime(str(time.values))

                # Calculate solar position for the specific time
                elev, decl = get_solar_position(mid_latitude, mid_longitude, datetime_obj)

                # Store the solar position for each time step
                solar_elevations.append(elev)
                declinations.append(decl)
                
            # Convert the lists into arrays with the same shape as the time dimension
            solar_elev_array = np.array(solar_elevations)
            decl_array = np.array(declinations)

            # Expand the arrays to match the spatial dimensions (time, y, x)
            solar_elev_broadcasted = xr.broadcast(
                xr.DataArray(solar_elev_array, dims=["time"], coords={"time": clipped_ds["time"]}),
                clipped_ds["y"], clipped_ds["x"]
            )[0]  # Take the first output (broadcasted solar elevation)

            decl_broadcasted = xr.broadcast(
                xr.DataArray(decl_array, dims=["time"], coords={"time": clipped_ds["time"]}),
                clipped_ds["y"], clipped_ds["x"]
            )[0]  # Take the first output (broadcasted declination)

            # Assign the broadcasted arrays to the dataset
            clipped_ds["SOLAR_ELEV"] = xr.DataArray(
                solar_elev_broadcasted.values,
                dims=("time", "y", "x"),
                coords={"time": clipped_ds["time"], "y": clipped_ds["y"], "x": clipped_ds["x"]},
            )
            clipped_ds["DECL"] = xr.DataArray(
                decl_broadcasted.values,
                dims=("time", "y", "x"),
                coords={"time": clipped_ds["time"], "y": clipped_ds["y"], "x": clipped_ds["x"]},
            )



            # Drop unused variables and keep only the variables of interest
            variables_of_interest.extend(["SOLAR_ELEV", "DECL"])
            clipped_ds = clipped_ds[variables_of_interest]

            # Save the selected data to a new NetCDF file
            clipped_ds.to_netcdf(output_path)

            print(f"Saved file: {output_path}")
