import xarray as xr
import pandas as pd
import os
import numpy as np
import random
from scipy.interpolate import griddata

def process_raster_to_dataframe(dataset_path, variable_name):
    ds = xr.open_dataset(dataset_path)
    data = ds['__xarray_dataarray_variable__'].values  # Extract the variable data
    x_coords = ds.coords["x"].values
    y_coords = ds.coords["y"].values
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    df =  pd.DataFrame({
        "x": x_grid.flatten(),
        "y": y_grid.flatten(),
        variable_name: data.flatten()
    })
    # Drop rows where data is NA
    df = df.dropna(subset=[variable_name])

    return df

def process_temporal_raster_to_dataframe(dataset_path, input_variables, output_variables):
    if len(input_variables) != len(output_variables):
        raise ValueError("The number of input_variables must match the number of output_variables.")
    
    ds = xr.open_dataset(dataset_path)
    time = ds.coords["time"].values
    x_coords = ds.coords["longitude"].values
    y_coords = ds.coords["latitude"].values

    # Create a DataFrame to hold all data
    all_data = []
    for t_index, t in enumerate(time):
        # Extract data for the current time step
        time_data = {"time": np.full(x_coords.size * y_coords.size, np.datetime_as_string(t, unit="s"))}
        for input_var, output_var in zip(input_variables, output_variables):
            if input_var not in ds:
                raise ValueError(f"Variable '{input_var}' not found in dataset.")
            var_data = ds[input_var][t_index, :, :].values
            time_data[output_var] = var_data.flatten()
        
        x_grid, y_grid = np.meshgrid(x_coords, y_coords)
        time_data["x"] = x_grid.flatten()
        time_data["y"] = y_grid.flatten()

        df = pd.DataFrame(time_data)
        df = df.dropna(subset=output_variables)  # Drop rows where any output variable is NA
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

def process_temporal_raster_xy_to_dataframe(dataset_path, input_variables, output_variables):
    if len(input_variables) != len(output_variables):
        raise ValueError("The number of input_variables must match the number of output_variables.")
    
    ds = xr.open_dataset(dataset_path)
    time = ds.coords["time"].values if "time" in ds.coords else None
    x_coords = ds.coords["x"].values if "x" in ds.coords else ds.coords["longitude"].values
    y_coords = ds.coords["y"].values if "y" in ds.coords else ds.coords["latitude"].values

    # Create a DataFrame to hold all data
    all_data = []
    for t_index, t in enumerate(time) if time is not None else [(0, None)]:
        time_data = {"time": np.full(x_coords.size * y_coords.size, np.datetime_as_string(t, unit="s"))} if time is not None else {}
        for input_var, output_var in zip(input_variables, output_variables):
            if input_var not in ds:
                raise ValueError(f"Variable '{input_var}' not found in dataset.")
            
            var_data = ds[input_var]
            if "time" in var_data.dims:
                # Index by time if the variable has a time dimension
                var_data = var_data.isel(time=t_index).values
            else:
                # Otherwise, take all data as is
                var_data = var_data.values

            if len(var_data.shape) == 2:  # If the data is already 2D
                time_data[output_var] = var_data.flatten()
            else:
                raise ValueError(f"Unexpected dimensions for variable '{input_var}': {var_data.shape}")

        x_grid, y_grid = np.meshgrid(x_coords, y_coords)
        time_data["x"] = x_grid.flatten()
        time_data["y"] = y_grid.flatten()

        df = pd.DataFrame(time_data)
        df = df.dropna(subset=output_variables)  # Drop rows where any output variable is NA
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

def process_geopot_raster_to_dataframe(dataset_path, input_var, output_var):
    
    # Open the dataset
    ds = xr.open_dataset(dataset_path)
    
    if input_var not in ds:
        raise ValueError(f"Variable '{input_var}' not found in dataset.")
        
    # Average the variable over the time dimension
    data_avg = ds[input_var].mean(dim="time", skipna = True).values.T
    ds = ds.drop('time')
    # Create a new DataArray with the correct dimensions (x, y)
    data_avg_da = xr.DataArray(data_avg, dims=["x", "y"], coords={"x": ds.coords["x"], "y": ds.coords["y"]})
    ds[input_var] = data_avg_da


    # Extract spatial coordinates
    x_coords = ds.coords["x"].values
    y_coords = ds.coords["y"].values
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    data = ds[input_var].values

    # Initialize the DataFrame with x and y
    df = pd.DataFrame({
        "x": x_grid.flatten(),
        "y": y_grid.flatten(),
        output_var: data.flatten()
    })

    df = df.dropna(subset=output_var)
    return df

# Helper function to replicate static data across time steps
def replicate_static_data(static_df, time_steps):
    replicated_data = pd.concat([static_df.assign(time=time) for time in time_steps])
    return replicated_data.reset_index(drop=True)

# Function to select 96 samples per month
def sample_per_month(group):
    if len(group) < 96:
        raise ValueError(f"Not enough timestamps ({len(group)}) in {group['year'].iloc[0]}-{group['month'].iloc[0]} to select 96.")
    return group.sample(n=96, random_state=42)

input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/Urbclim_percity'
ERA_solar_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/ERA_solar_interp_percity'
ERA_RH_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/ERA_RH_interp_percity'
coast_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/coast_new'
elev_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/elev_DMET_new'
height_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/height_new'
imperv_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/imperv_new'
population_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/population_new'
CORINE_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/CORINE_perc_new'
geopot_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/geopot_new'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/raster_total_CORINE_perc_ERA_interp'
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):
        print(f"Processing: {filename}")
        urbclim_path = os.path.join(input_directory, filename)
        urbclim_df = process_temporal_raster_xy_to_dataframe(urbclim_path, ["tas"], ["tas"])
        time_steps = urbclim_df["time"].unique()
        city_name = filename.replace('_total.nc', '')  # Extract city name from filename

        # Load datasets
        coast_path = os.path.join(coast_directory, 'coast_km1_' + city_name + ".nc")
        elev_path = os.path.join(elev_directory, 'elev_DMET_km1_' + city_name + ".nc")
        height_path = os.path.join(height_directory, 'height_km1_' + city_name + ".nc")
        imperv_path = os.path.join(imperv_directory, 'imperv_km1_' + city_name + ".nc")
        population_path = os.path.join(population_directory, 'population_km1_' + city_name + ".nc")
        ERA_path = os.path.join(ERA_solar_date_directory, city_name + '_ERA_solar_total.nc')
        ERA_RH_path = os.path.join(ERA_RH_date_directory, city_name + "_ERA_RH_total.nc")
        CORINE_path = os.path.join(CORINE_directory, 'CORINE_perc_km1_' + city_name + ".nc")
        geopot_path = os.path.join(geopot_directory, 'ERA5_geopot_km1_' + city_name + ".nc")
        output_file = os.path.join(output_directory, f"Total_{city_name}_CORINE_perc.csv")
        
        # Check if the file already exists
        if os.path.exists(output_file):
            continue  # Skip this iteration if file exists

        # Convert datasets to DataFrames
        # Process individual dataframes without replicating static data
        coast_df = process_raster_to_dataframe(coast_path, "COAST")
        elev_df = process_raster_to_dataframe(elev_path, "ELEV")
        height_df = process_raster_to_dataframe(height_path, "HEIGHT")
        imperv_df = process_raster_to_dataframe(imperv_path, "IMPERV")
        population_df = process_raster_to_dataframe(population_path, "POP")
        corine_df = process_temporal_raster_xy_to_dataframe(CORINE_path, ["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc"],
                                                                          ["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc"])
        geopot_df = process_geopot_raster_to_dataframe(geopot_path, 'z', 'GEOPOT')
       
        #for later interpolation purposes
        city_x = np.sort(height_df["x"].unique())
        city_y = np.sort(height_df["y"].unique())

        # Merge all static data by x and y
        static_data = coast_df     
        del coast_df
        static_data = static_data.merge(elev_df, on=["x", "y"], how="outer")
        del elev_df
        static_data = static_data.merge(height_df, on=["x", "y"], how="outer")
        del height_df
        static_data = static_data.merge(imperv_df, on=["x", "y"], how="outer")
        del imperv_df
        static_data = static_data.merge(population_df, on=["x", "y"], how="outer")
        del population_df
        static_data = pd.merge(static_data, geopot_df, on = ["x", "y"])
        del geopot_df
        static_data = static_data.merge(corine_df, on=["x", "y"], how="inner")
        del corine_df
        # Replicate static data after merging
        static_data = replicate_static_data(static_data, time_steps)

        ERA_df = process_temporal_raster_xy_to_dataframe(ERA_path, ["t2m", "blh", "sp", "tcc", "tp", "cape", "ssr", "ws", "SOLAR_ELEV", "DECL"],["T_2M", "BLH", "SP", "TCC", "PRECIP", "CAPE", "SSR","wind_speed", "SOLAR_ELEV", "DECL"])
        ERA_RH_df = process_temporal_raster_xy_to_dataframe(ERA_RH_path, ['r'],['RH'])
        
        # temporal subsampling
        #---------------------------------------------------------------------------------

        # Convert 'time' columns to datetime
        urbclim_df['time'] = pd.to_datetime(urbclim_df['time']).dt.round("H")
        ERA_df['time'] = pd.to_datetime(ERA_df['time']).dt.round("H")
        ERA_RH_df['time'] = pd.to_datetime(ERA_RH_df['time']).dt.round("H")

        # Determine overlap start and end
        overlap_start = max(urbclim_df['time'].min(), ERA_df['time'].min(), ERA_RH_df['time'].min())
        overlap_end = min(urbclim_df['time'].max(), ERA_df['time'].max(), ERA_RH_df['time'].max())

        # Get timestamps within the overlap period for all three datasets
        common_times = set(urbclim_df['time']).intersection(ERA_df['time'], ERA_RH_df['time'])

        # Filter times within the overlap range
        common_times = sorted([t for t in common_times if overlap_start <= t <= overlap_end])

        # Convert to DataFrame for easier grouping
        common_times_df = pd.DataFrame({'time': common_times})
        # Convert 'time' column to datetime 
        common_times_df['time'] = pd.to_datetime(common_times_df['time'])

        # Add year and month columns
        common_times_df['year'] = common_times_df['time'].dt.year
        common_times_df['month'] = common_times_df['time'].dt.month


        # Apply function to each (year, month) group
        selected_times_df = common_times_df.groupby(['year', 'month']).apply(sample_per_month).reset_index(drop=True)


        # Filter datasets based on selected times
        selected_times = set(selected_times_df['time'])
        urbclim_df = urbclim_df[urbclim_df['time'].isin(selected_times)]
        ERA_df = ERA_df[ERA_df['time'].isin(selected_times)]
        ERA_RH_df = ERA_RH_df[ERA_RH_df['time'].isin(selected_times)]

        # Ensure DataFrames are sorted by time
        urbclim_df = urbclim_df.sort_values('time').reset_index(drop=True)
        ERA_df = ERA_df.sort_values('time').reset_index(drop=True)
        ERA_RH_df = ERA_RH_df.sort_values('time').reset_index(drop=True)

        # Convert 'time' column back to string format (if necessary)
        urbclim_df['time'] = urbclim_df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        ERA_df['time'] = ERA_df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        ERA_RH_df['time'] = ERA_RH_df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        #spatially average ERA data

        # Compute spatial average for all variables except 'x' and 'y'
        #ERA_avg_values = ERA_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()
        #ERA_RH_avg_values = ERA_RH_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()

        # Merge back with original 'x' and 'y' to assign the same spatial average to each (x, y)
        #ERA_df = ERA_df[['time', 'x', 'y']].merge(ERA_avg_values, on='time', how='left')
        #ERA_RH_df = ERA_RH_df[['time', 'x', 'y']].merge(ERA_RH_avg_values, on='time', how='left')

        #------------------------------------------------------------------


        # Merge datasets on x, y, and time (replicating values for non-temporal datasets)
        combined_df = pd.merge(urbclim_df, static_data, on = ["x", "y", "time"], how = "inner")
        del static_data
        del urbclim_df
        combined_df = pd.merge(combined_df, ERA_df, on = ["x", "y", "time"], how = "inner")
        del ERA_df
        combined_df = pd.merge(combined_df, ERA_RH_df, on=["x", "y", "time"], how = "inner")
        del ERA_RH_df

        # spatial subsampling (2% of every LC class) --> doesn't work as we're working with percentage data.
        #---------------------------------------------------------------------------------
        #grouped_data = combined_df.groupby(["LC_CORINE", "time"])
        #combined_df = grouped_data.apply(lambda x: x.sample(frac=0.2)) # --> 20 instead of 2 percent as the resolution is also a lot lower (100m to 1km)
        #---------------------------------------------------------------------------------
        combined_df["T_2M_SL"] = combined_df['T_2M'] + 6.5*((combined_df['GEOPOT']/ 9.80665))/1000

        #now interpolate the T_2M_SL before recalculating it with lapse rate
        # Extract spatial and temporal dimensions
        df_time = combined_df["time"].unique()  # Get unique time steps
   

        # Create meshgrid for fine city grid
        city_lon_grid, city_lat_grid = np.meshgrid(city_x, city_y)

        # Prepare a list to store interpolated results
        interpolated_values = []

        # Loop over time steps
        for t in df_time:
            # Select data for current time step
            time_filtered = combined_df[combined_df["time"] == t]
            
            # Extract original points and values
            orig_points = np.column_stack([time_filtered["x"].values, time_filtered["y"].values])
            orig_values = time_filtered["T_2M_SL"].values
            
            # Interpolate
            interp_data = griddata(orig_points, orig_values, (city_lon_grid, city_lat_grid), method="linear")
            
            # Store results in a DataFrame
            interpolated_df = pd.DataFrame({
                "x": city_lon_grid.ravel(),
                "y": city_lat_grid.ravel(),
                "T_2M_SL": interp_data.ravel(),
                "time": t  # Add time column for merging later
            })
            
            interpolated_values.append(interpolated_df)
            


        # Combine all interpolated data
        interpolated_df = pd.concat(interpolated_values, ignore_index=True)

        # Merge back into combined_df (preserving other columns)
        combined_df = combined_df.drop(columns=["T_2M_SL"]).merge(interpolated_df, on=["x", "y", "time"], how="left")


        #perform the lapse rate correction
        combined_df["T_TARGET"] = combined_df['T_2M'] - 6.5*(combined_df['ELEV'])/1000
        combined_df = combined_df.drop(["GEOPOT"], axis = 1)

        combined_df.to_csv(output_file, index=False)
