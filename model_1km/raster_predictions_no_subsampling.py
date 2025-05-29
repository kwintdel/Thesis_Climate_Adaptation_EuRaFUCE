import os
import pandas as pd
import joblib

# Paths
models_path = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/models"
assignments_csv_path = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/train_combined.csv"
data_path = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/raster_total_no_subsampling"
output_path = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/raster_pred_no_subsampling"

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Load models
models = {
    1: joblib.load(os.path.join(models_path, "model_1km_CL1.joblib")),
    2: joblib.load(os.path.join(models_path, "model_1km_CL2.joblib")),
    3: joblib.load(os.path.join(models_path, "model_1km_CL3.joblib")),
}

# Load city-cluster assignments
city_assignments = pd.read_csv(assignments_csv_path)
city_assignments['Cluster'] = city_assignments['Cluster']+1

# Order of variables in the model
columns_order = ['LC_CORINE', 'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 
                 'RH', 'SP', 'PRECIP','T2M', 'WS', 'TCC',  'CAPE', 
                 'BLH', 'SSR','SOLAR_ELEV', 'DECL']

rename_mapping = {
            'T_2M': 'T2M',
            'wind_speed': 'WS'
        }
# Process each city
city = "Amsterdam"
# Iterate through files in the input directory
for i in [1,2]: #filename in os.listdir(input_directory):
    if i == 2:
        continue
    #assigned_cluster = city_assignments['Cluster'][city_assignments['City'] == city]
    assigned_cluster = 3
    # Path to the city's data file
    city_data_file = os.path.join(data_path, f"total_{city}.csv")
    
    if os.path.exists(city_data_file):
        # Load city data
        city_data = pd.read_csv(city_data_file)
        city_data = city_data.rename(columns = {"T_2M": "gone", 'T_TARGET': 'T_2M'})
        
        orig_rows = len(city_data)
        city_data = city_data.dropna()
        NA_rows = len(city_data)
        NA_diff = orig_rows - NA_rows
        print(f"city: {city}")
        print(f"amount of rows with NA/total amount of rows = {NA_diff} / {orig_rows}")
        if NA_diff == orig_rows:
            print("All rows are NA")
            continue

        city_loc = city_data[['x', 'y', 'time']]
        city_data = city_data.rename(columns = rename_mapping)
        city_data['T2M'] = city_data['T2M'] - 273.15
        city_data = city_data[columns_order]

        # Select the appropriate model
        model = models[assigned_cluster]
        print(f"model used: {assigned_cluster}")
        
        # Predict using the model
        predictions = model.predict(city_data)
        
        # Create a DataFrame for predictions
        predictions_df = pd.DataFrame(predictions, columns=["Prediction"])
        predictions_df['x'] = city_loc['x'].values
        predictions_df['y'] = city_loc['y'].values
        predictions_df['time'] = city_loc['time'].values
        
        
        # Save predictions to the output directory
        output_file = os.path.join(output_path, f"predictions_{city}.csv")
        predictions_df.to_csv(output_file, index=False)
        
        print(f"Predictions for {city} saved to: {output_file}")
    else:
        print(f"Data file for {city} not found: {city_data_file}")
