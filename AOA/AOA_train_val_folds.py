## create a file with all train and VAL cities of every cluster in and assign folds to later calculate the trainDI in R ##

import dask.dataframe as dd


## CLUSTER 1 ##

# File paths
train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER1_TRAIN_cities.csv"
VAL_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER1_VALIDATION_cities.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER1_TRAIN_VAL.csv"
folds_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/folds_CLUSTER1.csv"

# Read the train and VAL datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="64MB") 
VAL_ddf = dd.read_csv(VAL_file, blocksize="64MB")

# Add a column indicating the source
train_ddf["fold"] = 0
VAL_ddf["fold"] = 1

# Combine the datasets
combined_ddf = dd.concat([train_ddf, VAL_ddf])

# Save the combined data to a CSV file
combined_ddf.drop("fold", axis=1).to_csv(output_file, index=False, single_file=True)

# Save the folds to a separate file
combined_ddf[["fold"]].to_csv(folds_file, index=False, single_file=True)








## CLUSTER 2 ##

# File paths
train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER2_TRAIN_cities.csv"
VAL_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER2_VALIDATION_cities.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER2_TRAIN_VAL.csv"
folds_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/folds_CLUSTER2.csv"

# Read the train and VAL datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="64MB")  # Adjust blocksize as needed
VAL_ddf = dd.read_csv(VAL_file, blocksize="64MB")

# Add a column indicating the source
train_ddf["fold"] = 0
VAL_ddf["fold"] = 1

# Combine the datasets
combined_ddf = dd.concat([train_ddf, VAL_ddf])

# Save the combined data to a CSV file
combined_ddf.drop("fold", axis=1).to_csv(output_file, index=False, single_file=True)

# Save the folds to a separate file
combined_ddf[["fold"]].to_csv(folds_file, index=False, single_file=True)









## CLUSTER 3 ##


# File paths
train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER3_TRAIN_cities.csv"
VAL_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER3_VALIDATION_cities.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/CLUSTER3_TRAIN_VAL.csv"
folds_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/AOA/AOA_data/folds_CLUSTER3.csv"

# Read the train and VAL datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="64MB")  # Adjust blocksize as needed
VAL_ddf = dd.read_csv(VAL_file, blocksize="64MB")

# Add a column indicating the source
train_ddf["fold"] = 0
VAL_ddf["fold"] = 1

# Combine the datasets
combined_ddf = dd.concat([train_ddf, VAL_ddf])

# Save the combined data to a CSV file
combined_ddf.drop("fold", axis=1).to_csv(output_file, index=False, single_file=True)

# Save the folds to a separate file
combined_ddf[["fold"]].to_csv(folds_file, index=False, single_file=True)
print("Files have been combined and folds file created.")