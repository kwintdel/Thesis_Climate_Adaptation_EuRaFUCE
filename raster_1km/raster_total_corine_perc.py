import xarray as xr
import pandas as pd
import os
import numpy as np

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


# Helper function to check x and y consistency
def check_xy_consistency(dfs, names):
    reference_x = dfs[0]["x"]
    reference_y = dfs[0]["y"]
    
    for i, df in enumerate(dfs[1:], start=1):
        if not (df["x"].equals(reference_x) and df["y"].equals(reference_y)):
            print(f"Mismatch in x or y coordinates between {names[0]} and {names[i]}")
            print(f"Mismatched x rows in {names[i]}:\n{df.loc[~df['x'].isin(reference_x)]}")
            print(f"Mismatched y rows in {names[i]}:\n{df.loc[~df['y'].isin(reference_y)]}")

# Helper function to replicate static data across time steps
def replicate_static_data(static_df, time_steps):
    replicated_data = pd.concat([static_df.assign(time=time) for time in time_steps])
    return replicated_data.reset_index(drop=True)


# Updated directories
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_1km_results'
ERA_solar_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_solar_new_percity'
ERA_RH_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_RH_new_percity'
coast_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/coast_new'
elev_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/elev_DMET_new'
height_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/height_new'
imperv_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/imperv_new'
population_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/population_new'
CORINE_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/CORINE_perc_new'
geopot_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/geopot_new'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/raster_total'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a netCDF file
        print(f"Processing: {filename}")
        city_name = filename.replace('.nc', '')  # Extract city name from filename

        # Load datasets
        coast_path = os.path.join(coast_directory, 'coast_' + filename)
        elev_path = os.path.join(elev_directory, 'elev_DMET_' + filename)
        height_path = os.path.join(height_directory, 'height_' + filename)
        imperv_path = os.path.join(imperv_directory, 'imperv_' + filename)
        population_path = os.path.join(population_directory, 'population_' + filename)
        ERA_path = os.path.join(ERA_solar_date_directory, city_name + '_ERA_solar_total.nc')
        ERA_RH_path = os.path.join(ERA_RH_date_directory, city_name + '_ERA_RH_total.nc')
        CORINE_path = os.path.join(CORINE_directory, 'CORINE_perc_' + filename)
        geopot_path = os.path.join(geopot_directory, 'ERA5_geopot_' + filename)
        output_file = os.path.join(output_directory, f"total_{city_name}.csv")

        # Convert datasets to DataFrames
        coast_df = process_raster_to_dataframe(coast_path, "COAST")
        elev_df = process_raster_to_dataframe(elev_path, "ELEV")
        height_df = process_raster_to_dataframe(height_path, "HEIGHT")
        imperv_df = process_raster_to_dataframe(imperv_path, "IMPERV")
        population_df = process_raster_to_dataframe(population_path, "POP")
        ERA_df = process_temporal_raster_xy_to_dataframe(ERA_path, ["t2m", "blh", "sp", "tcc", "tp", "cape", "ssr", "ws", "SOLAR_ELEV", "DECL"],["T_2M", "BLH", "SP", "TCC", "PRECIP", "CAPE", "SSR","wind_speed", "SOLAR_ELEV", "DECL"])
        ERA_RH_df = process_temporal_raster_xy_to_dataframe(ERA_RH_path, ['r'],['RH'])
        corine_df = process_temporal_raster_xy_to_dataframe(CORINE_path, ["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc"],
                                                                          ["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc"])
        geopot_df = process_geopot_raster_to_dataframe(geopot_path, 'z', 'GEOPOT')

        time_steps = ERA_df["time"].unique()

        #spatially average ERA data

        # Compute spatial average for all variables except 'x' and 'y'
        ERA_avg_values = ERA_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()
        ERA_RH_avg_values = ERA_RH_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()

        # Merge back with original 'x' and 'y' to assign the same spatial average to each (x, y)
        ERA_df = ERA_df[['time', 'x', 'y']].merge(ERA_avg_values, on='time', how='left')
        ERA_RH_df = ERA_RH_df[['time', 'x', 'y']].merge(ERA_RH_avg_values, on='time', how='left')
        
        
        dataframes = [coast_df, elev_df, height_df, imperv_df, population_df, corine_df, ERA_df, ERA_RH_df, geopot_df]
        names = ["coast_df", "elev_df", "height_df", "imperv_df", "population_df", "corine_df", "ERA_df", "ERA_RH_df", "geopot_df"]
        check_xy_consistency(dataframes, names)
        
        # Merge datasets on x, y, and time (replicating values for non-temporal datasets)
        static_data = pd.merge(coast_df, elev_df, on=["x", "y"], how="inner")
        static_data = pd.merge(static_data, height_df, on=["x", "y"], how="inner")
        static_data = pd.merge(static_data, imperv_df, on=["x", "y"], how="inner")
        static_data = pd.merge(static_data, population_df, on=["x", "y"], how="inner")
        static_data = pd.merge(static_data, corine_df, on=["x", "y"], how="inner")
        static_data = pd.merge(static_data, geopot_df, on = ["x", "y"], how="inner")
        static_data = replicate_static_data(static_data, time_steps)

        # Merge with temporal datasets (ERA and ERA_RH)
        combined_df = pd.merge(ERA_df, ERA_RH_df, on=["x", "y", "time"], how="inner")
        combined_df = pd.merge(combined_df, static_data, on=["x", "y", "time"], how="inner")
        combined_df["T_TARGET"] = combined_df['T_2M']+6.5*((combined_df['GEOPOT']/ 9.80665))/1000 - 6.5*(combined_df['ELEV'])/1000

        combined_df = combined_df.drop(["GEOPOT"], axis = 1)
        

        # Save combined dataset to a single CSV file
        combined_df.to_csv(output_file, index=False)
