import xarray as xr
import pandas as pd
import os
import numpy as np

# Function to replace "tas_" with "coast"
def modify_variable_string(input_string):
    modified_string = 'char_' + input_string
    return modified_string

def calc_stats(input_path):
    overall_data = xr.open_dataset(input_path)  # Change this to the actual path of your CSV file
    # Extract the data array
    if "geopot" in input_path: 
        data_array = overall_data["z"].values
    else:
        data_array = overall_data["__xarray_dataarray_variable__"].values

    # Dictionary to store computed statistics for each column
    statistics = {}
    # Compute each statistic separately, skipping NaN values
    statistics['mean'] = np.nanmean(data_array)
    statistics['std'] = np.nanstd(data_array)
    statistics['min'] = np.nanmin(data_array)
    statistics['max'] = np.nanmax(data_array)
    statistics['25%'] = np.nanquantile(data_array, 0.25)
    statistics['75%'] = np.nanquantile(data_array, 0.75)
    statistics['median'] = np.nanquantile(data_array, 0.5)
    # Combine statistics into a single DataFrame
    tmp_df = pd.DataFrame([statistics])

    return tmp_df

# Define the input directory and output directory
input_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/rasters_results'
coast_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/coast_new'
elev_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/elev_new'
ERA_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/ERA_new'
ERA_RH_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/ERA_RH_new'
AHF_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/AHF_new'
geopot_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/geopot_new'
height_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/height_new'
imperv_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/imperv_new'
solar_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/solar_new'
population_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/population_new'
output_directory = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_EU/city_stats'

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.nc'):  # Check if the file is a netCDF file
        print(f"working on: {filename}")
        filename_new = modify_variable_string(filename)

        coast_path = os.path.join(coast_directory, 'coast_' + filename)
        elev_path = os.path.join(elev_directory, 'elev_' + filename)
        ERA_path = os.path.join(ERA_directory, 'ERA5_' + filename)
        ERA_RH_path = os.path.join(ERA_RH_directory, 'ERA5_RH_' + filename)
        AHF_path = os.path.join(AHF_directory, 'AHF_' + filename)
        geopot_path = os.path.join(geopot_directory, 'ERA5_geopot_' + filename)
        height_path = os.path.join(height_directory, 'height_' + filename)
        imperv_path = os.path.join(imperv_directory, 'imperv_' + filename)
        population_path = os.path.join(population_directory, 'population_' + filename)
        solar_path = os.path.join(solar_directory, 'solar_' + filename[:-3]+'.csv')
        output_path = os.path.join(output_directory, filename_new)

        # Calculate statistics for each variable
        coast_df = calc_stats(coast_path)
        coast_df.index = ["COAST"]
        elev_df = calc_stats(elev_path)
        elev_df.index = ["ELEV"]
        AHF_df = calc_stats(AHF_path)
        AHF_df.index = ["AHF"]
        geopot_df = calc_stats(geopot_path)
        geopot_df.index = ["GEOPOT"]
        height_df = calc_stats(height_path)
        height_df.index = ["HEIGHT"]
        imperv_df = calc_stats(imperv_path)
        imperv_df.index = ["IMPERV"]
        population_df = calc_stats(population_path)
        population_df.index = ["POP"]
        
        # Check for NaN values and print details
        for var_name, df in zip(['POP', 'HEIGHT', 'COAST', 'IMPERV', 'ELEV'], 
                                [population_df, height_df, coast_df, imperv_df, elev_df]):
            if df.isna().any(axis=None):  # Check if any NaN exists
                print(f"City: {filename}, Variable: {var_name}")
                print("Row with NaN values:")
                print(df[df.isna().any(axis=1)]) 

        # Load the CSV file for ERA5 data
        era5_df = pd.read_csv(ERA_path)
        # Set the 'Unnamed: 0' column as the index
        era5_df = era5_df.rename(columns={'Unnamed: 0': 'Variable'}).set_index('Variable')
        # Rename variables
        rename_mapping = {
            't2m': 'T_2M',
            'blh': 'BLH',
            'sp': 'SP',
            'tcc': 'TCC',
            'tp': 'PRECIP',
            'ws': 'wind_speed',
            'ssr': 'SSR',
            'cape': 'CAPE'
        }
        era5_df = era5_df.rename(index=rename_mapping)

        era5_df['std'] = None  # Placeholder for standard deviation
        era5_df['25%'] = None  # Placeholder for 25th percentile
        era5_df['75%'] = None  # Placeholder for 75th percentile

        # Reorder rows according to the specified order
        desired_order = ['SP', 'PRECIP', 'T_2M', 'wind_speed', 'TCC', 'BLH', 'CAPE']
        era5_df = era5_df.loc[desired_order]

        # Reorder columns to match the desired format
        era5_df = era5_df[['mean', 'std', 'min', 'max', '25%', '75%', 'median']]

        # Load the CSV file for ERA5 RH data
        era5_RH_df = pd.read_csv(ERA_RH_path)
        # Set the 'Unnamed: 0' column as the index
        era5_RH_df = era5_RH_df.rename(columns={'Unnamed: 0': 'Variable'}).set_index('Variable')
        # Rename variables
        rename_mapping = {
            'r': 'RH'
        }
        era5_RH_df = era5_RH_df.rename(index=rename_mapping)

        era5_RH_df['std'] = None  # Placeholder for standard deviation
        era5_RH_df['25%'] = None  # Placeholder for 25th percentile
        era5_RH_df['75%'] = None  # Placeholder for 75th percentile
        # Reorder columns to match the desired format
        era5_RH_df = era5_RH_df[['mean', 'std', 'min', 'max', '25%', '75%', 'median']]


        # Load the CSV file for solar data
        solar_df = pd.read_csv(solar_path, index_col = 0)

        solar_df['mean'] = None  # Placeholder for mean
        solar_df['std'] = None  # Placeholder for standard deviation
        solar_df['min'] = None  # Placeholder for minimum
        solar_df['25%'] = None  # Placeholder for 25th percentile
        solar_df['75%'] = None  # Placeholder for 75th percentile
        # Reorder columns to match the desired format
        solar_df = solar_df[['mean', 'std', 'min', 'max', '25%', '75%', 'median']]

        # Combine all dataframes
        combined_df = pd.concat([height_df, coast_df, imperv_df, elev_df, population_df, era5_RH_df, era5_df, solar_df, geopot_df, AHF_df], axis=0)
        combined_df.loc['PRECIP'] *= 10000
        combined_df.loc['T_TARGET'] = combined_df.loc['T_2M']+6.5*((combined_df.loc['GEOPOT']/ 9.80665))/1000 - 6.5*(combined_df.loc['ELEV'])/1000
        combined_df.index.name = 'Variable'

        # Save to output
        combined_df.to_csv(output_path)
