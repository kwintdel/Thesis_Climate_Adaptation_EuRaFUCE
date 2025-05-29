import os
import pandas as pd

# File paths
rasters_dir = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/raster_total"

citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER1_TRAIN_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER1_TRAIN_1km.csv"

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")


# New file paths
citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER1_VALIDATION_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER1_VALIDATION_1km.csv"

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")


citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER1_TEST_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER1_TEST_1km.csv"

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")


# New file paths
citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER2_TRAIN_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER2_TRAIN_1km.csv"

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")



# New file paths
citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER2_VALIDATION_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER2_VALIDATION_1km.csv"

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")



citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER2_TEST_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER2_TEST_1km.csv"

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")



# New file paths
citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER3_TRAIN_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER3_TRAIN_1km.csv"

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")




# New file paths
citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER3_VALIDATION_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER3_VALIDATION_1km.csv"

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")



citynames_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val_names/CLUSTER3_TEST_citynames.csv"
output_file = "/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/model_1km/train_val/CLUSTER3_TEST_1km.csv"

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read city names
citynames_df = pd.read_csv(citynames_file)
citynames = citynames_df['city'].tolist()

# Step 2: Prepare output file (create header)
header_written = False

# Step 3: Process each city file
for city in citynames:
    city_file = os.path.join(rasters_dir, f"Total_{city}.csv")

    if os.path.exists(city_file):
        # Read entire file at once
        df = pd.read_csv(city_file)
        
        # Add city column
        df['city'] = city
        
        # Write to output file
        df.to_csv(output_file, mode='a', index=False, header=not header_written)
        header_written = True  # Ensure header is written only once
    else:
        print(f"Warning: File not found for city {city}")