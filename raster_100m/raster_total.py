import xarray as xr
import pandas as pd
import os
import numpy as np

# Mapping from CORINE (1-44) to UrbClim (1-15)
corine_to_urbclim = {
    1: 1, # Urban
    2: 2, # Sub-urban
    3: 3, 4: 3, 5: 3, 6: 3,  # Industrial
    10: 4, 11: 4,  # Urban green
    34: 5,  # Snow/Ice
    8: 6, 9: 6, 30: 6, 31: 6, 38: 6, 39: 6,  # Bare soil
    7: 7, 18: 7, 26: 7, 27: 7, 32: 7, 35: 7, 36: 7, 37: 7,  # Grassland
    12: 8, 13: 8, 14: 8, 19: 8, 20: 8, 21: 8,  # Cropland
    15: 9, 28: 9, 29: 9, 33: 9,  # Shrubland
    16: 10, 17: 10, 22: 10,  # Woodland
    23: 11, 25: 11,  # Broadleaf trees
    24: 12,  # Needleleaf trees
    40: 13,  # Rivers
    41: 14,  # Inland water bodies
    42: 15, 43: 15, 44: 15  # Sea
}
def process_raster_to_dataframe(dataset_path, variable_name):
    ds = xr.open_dataset(dataset_path)
    data = ds["__xarray_dataarray_variable__"].values

    x_coords = ds.coords["x"].values
    y_coords = ds.coords["y"].values
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    return pd.DataFrame({
        "x": x_grid.flatten(),
        "y": y_grid.flatten(),
        variable_name: data.flatten()
    })

def process_temporal_raster_to_dataframe(dataset_path, input_variables, output_variables):
    if len(input_variables) != len(output_variables):
        raise ValueError("The number of input_variables must match the number of output_variables.")
    
    ds = xr.open_dataset(dataset_path)
    data = ds[input_variables].values
    time = ds.coords["time"].values
    time = np.datetime_as_string(time, unit="s")
    x_coords = ds.coords["longitude"].values
    y_coords = ds.coords["latitude"].values
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    time_array = np.array([time] * x_grid.size)

    # Initialize the DataFrame with x, y, and time
    df = pd.DataFrame({
        "x": x_grid.flatten(),
        "y": y_grid.flatten(),
        "time": time_array
    })

    # Add each variable to the DataFrame with renaming
    for input_var, output_var in zip(input_variables, output_variables):
        if input_var not in ds:
            raise ValueError(f"Variable '{input_var}' not found in dataset.")
        data = ds[input_var].values  # Extract the variable's data
        df[output_var] = data.flatten()  # Add the variable as a renamed column

    return df

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

def process_geopot_raster_to_dataframe(dataset_path, input_variables, output_variables):
    if len(input_variables) != len(output_variables):
        raise ValueError("The number of input_variables must match the number of output_variables.")
    
    # Open the dataset
    ds = xr.open_dataset(dataset_path)
    
    # Extract spatial coordinates
    x_coords = ds.coords["x"].values
    y_coords = ds.coords["y"].values
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    # Initialize the DataFrame with x and y
    df = pd.DataFrame({
        "x": x_grid.flatten(),
        "y": y_grid.flatten()
    })
    
    # Process each variable: average over time and add to DataFrame
    for input_var, output_var in zip(input_variables, output_variables):
        if input_var not in ds:
            raise ValueError(f"Variable '{input_var}' not found in dataset.")
        
        # Average the variable over the time dimension
        data_avg = ds[input_var].mean(dim="time").values
        
        # Add the averaged variable to the DataFrame
        df[output_var] = data_avg.flatten()

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
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
ERA_solar_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/ERA_solar_new_percity'
ERA_RH_date_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/ERA_RH_new_percity'
coast_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/coast_new'
elev_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/elev_DMET_new'
height_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/height_new'
imperv_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/imperv_new'
population_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/population_new'
CORINE_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/CORINE_new'
geopot_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/geopot_new'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/raster_total'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)
#filename = "Bruges.nc"
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
        CORINE_path = os.path.join(CORINE_directory, 'CORINE_' + filename)
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
        geopot_df = process_geopot_raster_to_dataframe(geopot_path, ['z'], ['GEOPOT'])

        time_steps = ERA_df["time"].unique()

        #spatially average ERA data

        # Compute spatial average for all variables except 'x' and 'y'
        ERA_avg_values = ERA_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()
        ERA_RH_avg_values = ERA_RH_df.drop(columns=['x', 'y']).groupby("time").mean().reset_index()

        # Merge back with original 'x' and 'y' to assign the same spatial average to each (x, y)
        ERA_df = ERA_df[['time', 'x', 'y']].merge(ERA_avg_values, on='time', how='left')
        ERA_RH_df = ERA_RH_df[['time', 'x', 'y']].merge(ERA_RH_avg_values, on='time', how='left')

        # Process CORINE data
        corine_ds = xr.open_dataset(CORINE_path)
        corine_data = corine_ds["__xarray_dataarray_variable__"].values.flatten() 

        # Map CORINE classes to UrbClim classes
        urbclim_classes = [corine_to_urbclim.get(value, 0) for value in corine_data] 

        # Ensure x, y, and LC_CORINE align correctly
        x_coords = corine_ds.coords["x"].values
        y_coords = corine_ds.coords["y"].values
        x_grid, y_grid = np.meshgrid(x_coords, y_coords)  # Create 2D grids of x and y
        flattened_x = x_grid.flatten()
        flattened_y = y_grid.flatten()

        # Create a DataFrame for CORINE data
        corine_df = pd.DataFrame({
            "x": flattened_x,
            "y": flattened_y,
            "LC_CORINE": urbclim_classes
        })
        
        dataframes = [coast_df, elev_df, height_df, imperv_df, population_df, corine_df, ERA_df, ERA_RH_df, geopot_df]
        names = ["coast_df", "elev_df", "height_df", "imperv_df", "population_df", "corine_df", "ERA_df", "ERA_RH_df", "geopot_df"]
        check_xy_consistency(dataframes, names)
        
        # Merge datasets on x, y, and time (replicating values for non-temporal datasets)
        static_data = pd.merge(coast_df, elev_df, on=["x", "y"], how = "inner")
        static_data = pd.merge(static_data, height_df, on=["x", "y"], how = "inner")
        static_data = pd.merge(static_data, imperv_df, on=["x", "y"], how = "inner")
        static_data = pd.merge(static_data, population_df, on=["x", "y"], how = "inner")
        static_data = pd.merge(static_data, corine_df, on=["x", "y"], how = "inner")
        static_data = pd.merge(static_data, geopot_df, on = ["x", "y"], how = "inner")
        static_data = replicate_static_data(static_data, time_steps)

        # Merge with temporal datasets (ERA and ERA_RH)
        combined_df = pd.merge(ERA_df, ERA_RH_df, on=["x", "y", "time"], how = "inner")
        combined_df = pd.merge(combined_df, static_data, on=["x", "y", "time"], how = "inner")
        combined_df["T_TARGET"] = combined_df['T_2M']+6.5*((combined_df['GEOPOT']/ 9.80665))/1000 - 6.5*(combined_df['ELEV'])/1000

        combined_df = combined_df.drop(["GEOPOT"], axis = 1)
        

        # Save combined dataset to a single CSV file
        combined_df.to_csv(output_file, index=False)
