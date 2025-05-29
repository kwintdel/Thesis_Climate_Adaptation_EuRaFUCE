import xarray as xr
import numpy as np
import rasterio as rio
import rioxarray as rxr
import os
import ephem
import pandas as pd
from scipy.interpolate import griddata

# Specify the directories
era_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/data/ERA'
city_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_1km_results'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_solar_interp_sep'

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

# Loop over all ERA5 files in era_dir
for era5_file in os.listdir(era_dir):
    if era5_file.endswith(".nc"):
        print(f"Working on: {era5_file}")

        # Open the ERA5 file, assign a CRS and rename coordinates to match city files
        era5_path = os.path.join(era_dir, era5_file)
        ds = xr.open_dataset(era5_path).rio.write_crs("EPSG:4326")
        ds = ds.rename({"longitude": "x", "latitude": "y"})
        date = era5_file[5:-3]

        # We remove the pre-interpolation calculations of ws and tp.
        # Instead, we add v10 and u10 to the list so that they are interpolated.
        variables_of_interest = ["blh", "sp", "tcc", "tp", "cape", "ssr", "v10", "u10"]

        # Loop over all city files in the city_dir
        for city_file in os.listdir(city_dir):
            print(f"Processing city file: {city_file}")
            city_file_path = os.path.join(city_dir, city_file)
            city = xr.open_dataset(city_file_path)
            # Extract city name from the file name
            city_name = city_file[0:-3]

            # Create the output directory for the city if it doesn't exist
            city_output_dir = os.path.join(output_dir, city_name)
            os.makedirs(city_output_dir, exist_ok=True)
            output_filename = f"{city_name}_ERA5_solar_{date}_new.nc"
            output_path = os.path.join(city_output_dir, output_filename)
            # Check if the file already exists
            if os.path.exists(output_path):
                continue  # Skip this iteration if file exists

            # Get target (fine) grid from the city file
            city_x = city["x"].values  # 1 km resolution x
            city_y = city["y"].values  # 1 km resolution y

            # Determine the bounding box of the city (plus a 1° buffer)
            lon_min, lon_max = city_x.min(), city_x.max()
            lat_min, lat_max = city_y.min(), city_y.max()

            # Use the ERA5 dataset’s coordinates to select a subset that covers the city
            ds_x = ds["x"].values
            ds_y = ds["y"].values
            lon_mask = (ds_x >= lon_min - 1) & (ds_x <= lon_max + 1)
            lat_mask = (ds_y >= lat_min - 1) & (ds_y <= lat_max + 1)
            subset_x = ds_x[lon_mask]
            subset_y = ds_y[lat_mask]

            # Create meshgrids for the coarse grid (subset) and the fine city grid
            coarse_lon_grid, coarse_lat_grid = np.meshgrid(subset_x, subset_y)
            city_lon_grid, city_lat_grid = np.meshgrid(city_x, city_y)

            # Prepare a dictionary to hold the interpolated variables
            interp_vars = {}

            # Loop over each variable to be interpolated, do not interpolate t2m, we will do this later after applying the correction with the geopotential.
            for var in variables_of_interest:
                print(f"  Interpolating variable: {var}")
                # Subset the variable to the coarse grid region
                var_data = ds[var].sel(x=subset_x, y=subset_y)
                # Get the number of time steps (assumed to be the first dimension)
                time_dim = var_data.shape[0]
                # Convert to a NumPy array: shape (time, lat, lon)
                var_data_np = var_data.values
                # Prepare an array to hold the interpolated data for all time steps
                interp_data = np.empty((time_dim, city_lon_grid.shape[0], city_lon_grid.shape[1]))
                # Prepare the list of original coarse grid points (same for every time step)
                orig_points = np.column_stack([coarse_lon_grid.ravel(), coarse_lat_grid.ravel()])
                # Loop over each time step
                for t in range(time_dim):
                    orig_values = var_data_np[t].ravel()
                    interp_data[t] = griddata(orig_points,
                                              orig_values,
                                              (city_lon_grid, city_lat_grid),
                                              method="linear")
                # Create a DataArray with dimensions (time, y, x) for the interpolated variable
                interp_vars[var] = xr.DataArray(interp_data,
                                                dims=["time", "y", "x"],
                                                coords={"time": var_data["time"],
                                                        "y": city_y,
                                                        "x": city_x})
            # Create a new Dataset from the interpolated variables
            interp_ds = xr.Dataset(interp_vars)


            # Select the nearest values from the ERA5 grid to the city grid
            # This ensures t2m aligns exactly with the city grid without interpolation
            t2m_nn = ds["t2m"].sel(
                x=xr.DataArray(city_x, dims="x"),
                y=xr.DataArray(city_y, dims="y"),
                method="nearest"
            )

            # Just to be sure, sort and drop any duplicates (rare but for safety)
            unique_y, unique_y_idx = np.unique(city_y, return_index=True)
            unique_x, unique_x_idx = np.unique(city_x, return_index=True)

            # Ensure that final assignment is aligned to the expected shape (time, y, x)
            t2m_nn = t2m_nn.isel(
                x=unique_x_idx,
                y=unique_y_idx
            )

            # Assign to dataset
            interp_ds["t2m"] = xr.DataArray(
                t2m_nn.values,
                dims=["time", "y", "x"],
                coords={"time": t2m_nn["time"], "y": city_y[unique_y_idx], "x": city_x[unique_x_idx]}
            )

            # Now compute derived variables after interpolation.
            # Compute ws from interpolated v10 and u10.
            interp_ds["ws"] = np.sqrt(interp_ds["v10"]**2 + interp_ds["u10"]**2)
            # Convert tp to mm/h (assuming the original units require this conversion)
            interp_ds["tp"] = interp_ds["tp"] * 1000

            # Optionally, you can drop v10 and u10 if they are no longer needed:
            interp_ds = interp_ds.drop_vars(["v10", "u10"])

            # Calculate solar positions on the interpolated grid.
            # Use the average city coordinates as the location for solar position calculation.
            mid_latitude = np.mean(city_y)
            mid_longitude = np.mean(city_x)
            solar_elevations = []
            declinations = []
            for t in interp_ds["time"]:
                datetime_obj = pd.to_datetime(str(t.values))
                elev, decl = get_solar_position(mid_latitude, mid_longitude, datetime_obj)
                solar_elevations.append(elev)
                declinations.append(decl)
            solar_elev_array = np.array(solar_elevations)
            decl_array = np.array(declinations)
            # Broadcast the 1D solar arrays to the (time, y, x) grid
            solar_elev_broadcasted = xr.broadcast(
                xr.DataArray(solar_elev_array, dims=["time"], coords={"time": interp_ds["time"]}),
                interp_ds["y"], interp_ds["x"]
            )[0]
            decl_broadcasted = xr.broadcast(
                xr.DataArray(decl_array, dims=["time"], coords={"time": interp_ds["time"]}),
                interp_ds["y"], interp_ds["x"]
            )[0]

            # Add the solar position variables to the dataset
            interp_ds["SOLAR_ELEV"] = xr.DataArray(
                solar_elev_broadcasted.values,
                dims=("time", "y", "x"),
                coords={"time": interp_ds["time"], "y": interp_ds["y"], "x": interp_ds["x"]}
            )
            interp_ds["DECL"] = xr.DataArray(
                decl_broadcasted.values,
                dims=("time", "y", "x"),
                coords={"time": interp_ds["time"], "y": interp_ds["y"], "x": interp_ds["x"]}
            )

            # Define final variable order.
            # Now final variables include all the interpolated ones plus the derived ones.
            final_vars = ["t2m", "blh", "sp", "tcc", "tp", "cape", "ssr", "ws", "SOLAR_ELEV", "DECL"]
            interp_ds = interp_ds[final_vars]

            # Save the dataset to a new NetCDF file
            interp_ds.to_netcdf(output_path)
            print(f"Saved file: {output_path}")
