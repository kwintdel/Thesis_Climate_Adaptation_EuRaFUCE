import pandas as pd
import numpy as np
import glob

# Define the directory and file pattern
file_path_pattern = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/*_train.csv'

# Find all files matching the pattern
file_paths = glob.glob(file_path_pattern)

# Initialize an empty list for DataFrames
dataframes = []

# Load each file and process if needed
for file in file_paths:
    df = pd.read_csv(file)
    # Special processing for 'average_coast_train.csv'
    if 'average_coast_train.csv' in file:
        df['City'] = df['City'].str.replace('.nc', '', regex=False)
        df['Average_Coast_Band_Value'] = np.log10(df['Average_Coast_Band_Value'])
    if 'average_lat_lon_cluster_train.csv' in file:
        df['City'] = df['City'].apply(lambda x: x.split('_')[0])
    dataframes.append(df)

# Perform a series of inner joins on the 'City' column
merged_data = dataframes[0]
for df in dataframes[1:]:
    merged_data = pd.merge(merged_data, df, on='City', how='inner')

merged_data = merged_data.drop(['function'], axis=1)

# Rename the columns for clarity
merged_data = merged_data.rename(columns={
    'Average_PRECIP': 'PRECIP',
    'Average_T_TARGET': 'T_TARGET',
    'Average_AHF_Band_Value': 'AHF',
    'Average_Coast_Band_Value': 'COAST',
    'Average_Elevation_Band_Value': 'ELEV'
})

merged_data['ELEV'] = merged_data['ELEV']/1000
merged_data['PRECIP'] = merged_data['PRECIP']*1000
# Save the combined DataFrame to a new CSV file
output_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/train_combined.csv'
merged_data.to_csv(output_path, index=False)

print(f"Combined file saved to {output_path}")
