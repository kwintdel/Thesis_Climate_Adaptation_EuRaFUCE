import dask.dataframe as dd
import dask.array as da
import pandas as pd
import os

data_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names"
os.makedirs(data_file, exist_ok=True)

train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER1_TRAIN_cities.csv"
val_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER1_VALIDATION_cities.csv"
test_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER1_TEST_cities.csv"

# Read the train and val datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="256MB")
val_ddf = dd.read_csv(val_file, blocksize="256MB")
test_ddf =dd.read_csv(test_file, blocksize="256MB")

# Get unique cities from both train and val datasets
train_cities = train_ddf["city"].unique().compute()
val_cities = val_ddf["city"].unique().compute()
test_cities = test_ddf["city"].unique().compute()

# Convert the unique cities to a pandas DataFrame
train_cities_df = pd.DataFrame(train_cities, columns=["city"])
val_cities_df = pd.DataFrame(val_cities, columns = ["city"])
test_cities_df = pd.DataFrame(test_cities, columns = ["city"])

# Save the unique city names to CSV
train_cities_df.to_csv(data_file + '/CLUSTER1_TRAIN_citynames.csv', index=False)
val_cities_df.to_csv(data_file + '/CLUSTER1_VALIDATION_citynames.csv', index=False)
test_cities_df.to_csv(data_file + '/CLUSTER1_TEST_citynames.csv', index=False)







train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER2_TRAIN_cities.csv"
val_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER2_VALIDATION_cities.csv"
test_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER2_TEST_cities.csv"

# Read the train and val datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="256MB")
val_ddf = dd.read_csv(val_file, blocksize="256MB")
test_ddf = dd.read_csv(test_file, blocksize="256MB")

# Get unique cities from both train and val datasets
train_cities = train_ddf["city"].unique().compute()
val_cities = val_ddf["city"].unique().compute()
test_cities = test_ddf["city"].unique().compute()

# Convert the unique cities to a pandas DataFrame
train_cities_df = pd.DataFrame(train_cities, columns=["city"])
val_cities_df = pd.DataFrame(val_cities, columns = ["city"])
test_cities_df = pd.DataFrame(test_cities, columns = ["city"])

# Save the unique city names to CSV
train_cities_df.to_csv(data_file + '/CLUSTER2_TRAIN_citynames.csv', index=False)
val_cities_df.to_csv(data_file + '/CLUSTER2_VALIDATION_citynames.csv', index=False)
test_cities_df.to_csv(data_file + '/CLUSTER2_TEST_citynames.csv', index=False)






train_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER3_TRAIN_cities.csv"
val_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER3_VALIDATION_cities.csv"
test_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_data/CLUSTER3_TEST_cities.csv"

# Read the train and val datasets using Dask
train_ddf = dd.read_csv(train_file, blocksize="256MB")
val_ddf = dd.read_csv(val_file, blocksize="256MB")
test_ddf = dd.read_csv(test_file, blocksize="256MB")

# Get unique cities from both train and val datasets
train_cities = train_ddf["city"].unique().compute()
val_cities = val_ddf["city"].unique().compute()
test_cities = test_ddf["city"].unique().compute()

# Convert the unique cities to a pandas DataFrame
train_cities_df = pd.DataFrame(train_cities, columns=["city"])
val_cities_df = pd.DataFrame(val_cities, columns = ["city"])
test_cities_df = pd.DataFrame(test_cities, columns = ["city"])

# Save the unique city names to CSV
train_cities_df.to_csv(data_file + '/CLUSTER3_TRAIN_citynames.csv', index=False)
val_cities_df.to_csv(data_file + '/CLUSTER3_VALIDATION_citynames.csv', index=False)
test_cities_df.to_csv(data_file + '/CLUSTER3_TEST_citynames.csv', index=False)