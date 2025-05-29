import os
import numpy as np  
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_squared_error
import joblib
import time


# Define functions for MAE, MSE, and correlation (R-squared)
def calculate_mae(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)

def calculate_mse(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)

def calculate_correlation(y_true, y_pred):
    return r2_score(y_true, y_pred)

def calculate_bias(y_pred, y_true):
    return ((y_pred - y_true).mean())

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_ERA_interp/CLUSTER2_TEST_1km.csv'
val = pd.read_csv(file_path, usecols=[ 'city','tas', 'T_TARGET', "LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc",
                                                                            'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP', 'wind_speed', 'TCC', 'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL'], low_memory=False)

file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_ERA_interp/CLUSTER2_TRAIN_1km.csv'
train = pd.read_csv(file_path, usecols=['city','tas', 'T_TARGET',"LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc",
                                                                            'IMPERV', 'HEIGHT',  'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP', 'wind_speed', 'TCC', 'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL'], low_memory=False)

train = train.rename(columns={'T_TARGET': 'T2M', 'tas': 'T_TARGET', 'wind_speed': 'WS'})
val = val.rename(columns={'T_TARGET': 'T2M', 'tas': 'T_TARGET', 'wind_speed': 'WS'})

# Count NaN values per column before dropping
val_nan_before_drop = val.isnull().sum()
train_nan_before_drop = train.isnull().sum()

# Drop rows with NaN values in 'T_TARGET' column
val = val.dropna(subset=['T_TARGET'])
train = train.dropna(subset=['T_TARGET'])
#no clue why the following two lines are necessary and aren't for val, but it works now so euhm hands off.
train['T_TARGET'] = pd.to_numeric(train['T_TARGET'], errors='coerce')
train['T2M'] = pd.to_numeric(train['T2M'], errors='coerce')

val['T_TARGET'] = pd.to_numeric(val['T_TARGET'], errors='coerce')
val['T2M'] = pd.to_numeric(val['T2M'], errors='coerce')

val['T2M_difference'] = val['T_TARGET'] - val['T2M']
val['T2M'] = val['T2M'] - 273.15
train['T2M_difference'] = train['T_TARGET'] - train['T2M']
train['T2M'] = train['T2M'] - 273.15

train = train.dropna(subset=['T2M_difference'])
val = val.dropna(subset=['T2M_difference'])

# Count NaN values per column after dropping 'T_TARGET'
val_nan_after_drop = val.isnull().sum()
train_nan_after_drop = train.isnull().sum()

start_time = time.perf_counter()
# Fill NaN values with the median value of the specific 'City'
for column in val.columns:
    if val[column].isnull().any():
        val[column] = val.groupby('city')[column].transform(lambda x: x.fillna(x.median()))

for column in train.columns:
    if train[column].isnull().any():
        train[column] = train.groupby('city')[column].transform(lambda x: x.fillna(x.median()))

end_time = time.perf_counter()
elapsed_time = end_time - start_time

# Write results to file
with open('run_time_CL2_ERA_interp.txt', 'a') as f:
    f.write(f"Elapsed time impute:  {elapsed_time} seconds  \n")




# Count NaN values per column after filling with median
val_nan_after_median_fill = val.isnull().sum()
train_nan_after_median_fill = train.isnull().sum()

# Calculate number of NaN values filled and dropped per column
val_nan_filled = val_nan_before_drop - val_nan_after_drop
train_nan_filled = train_nan_before_drop - train_nan_after_drop

val_nan_dropped = val_nan_after_drop - val_nan_after_median_fill
train_nan_dropped = train_nan_after_drop - train_nan_after_median_fill

# Writing results to a file
with open('run_time_CL2_ERA_interp.txt', 'a') as f:
    f.write("NaN values filled per column before dropping 'T_TARGET':\n")
    f.write("Validation Data:\n")
    f.write(val_nan_filled.to_string() + "\n")
    f.write("Training Data:\n")
    f.write(train_nan_filled.to_string() + "\n")
    f.write("\n")
    f.write("NaN values dropped per column after dropping 'T_TARGET':\n")
    f.write("Validation Data:\n")
    f.write(val_nan_dropped.to_string() + "\n")
    f.write("Training Data:\n")
    f.write(train_nan_dropped.to_string() + "\n")

y_train = train['T2M_difference']
train = train[["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc",
                                                                            'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP','T2M', 'WS', 'TCC',  'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL']]

y_val = val['T2M_difference'] 
val = val[["LC_1_perc", "LC_2_perc", "LC_3_perc", "LC_4_perc", "LC_5_perc", 
                                                                          "LC_6_perc", "LC_7_perc", "LC_8_perc", "LC_9_perc", "LC_10_perc", 
                                                                          "LC_11_perc", "LC_12_perc", "LC_13_perc", "LC_14_perc", "LC_15_perc",
                                                                            'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP','T2M', 'WS', 'TCC',  'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL']]

#checked and the following are the same of the original model
max_depth = 12     
n_estimators = 20  
max_features = 0.33   

# Create a RandomForestRegressor with the current parameters
rf = RandomForestRegressor(
     max_depth=max_depth,
     n_estimators=n_estimators,
     max_features=max_features,
     n_jobs=-1,
     random_state=42
   )

start_time = time.perf_counter()

with joblib.parallel_backend(backend='loky', n_jobs=-1):
    rf.fit(train, y_train)

# Fit the model on the training data
y_pred_train = rf.predict(train)

# Make predictions on the test set

# Make predictions on the validation set
y_pred_val = rf.predict(val)

# Evaluate the model on the datasets
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))

mae_train= calculate_mae(y_train, y_pred_train)
mae_val= calculate_mae(y_val, y_pred_val)


mse_train= calculate_mse(y_train, y_pred_train)
mse_val= calculate_mse(y_val, y_pred_val)


correlation_train=  calculate_correlation(y_train, y_pred_train)
correlation_val= calculate_correlation(y_val, y_pred_val)

bias_train= calculate_bias(y_train, y_pred_train)
bias_val= calculate_bias(y_val, y_pred_val)




end_time = time.perf_counter()
elapsed_time = end_time - start_time
with open('run_time_CL2_ERA_interp.txt', 'a') as f:
    f.write(f"Elapsed time model : {elapsed_time} seconds and rmse val score of {rmse_val} and rmse train score of {rmse_train} \n")
    f.write(f"Elapsed time model: {elapsed_time} seconds and mae val score of {mae_val} and mae train score of {mae_train} \n")
    f.write(f"Elapsed time model: {elapsed_time} seconds and mse val score of {mse_val} and mse train score of {mse_train} \n")
    f.write(f"Elapsed time model: {elapsed_time} seconds and bias val score of {bias_val} and bias train score of {bias_train} \n")
    f.write(f"Elapsed time model: {elapsed_time} seconds and correlation val score of {correlation_val} and correlation train score of {correlation_train} \n")


joblib.dump(rf, "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/models/model_1km_CL2_ERA_interp.joblib")

