import os
import xarray as xr

# Define the directories
input_base_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_RH_new_sep'
output_dir = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/raster_1km/ERA_RH_new_percity'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop over all city folders in the input base directory
for city_folder in os.listdir(input_base_dir):
    city_path = os.path.join(input_base_dir, city_folder)
    if os.path.isdir(city_path):  # Ensure it is a folder
        city_files = [os.path.join(city_path, f) for f in os.listdir(city_path) if f.endswith('.nc')]
        
        # Combine all files for the current city
        datasets = [xr.open_dataset(file) for file in city_files]
        combined_dataset = xr.concat(datasets, dim="time") 
        
        # Close individual datasets to free resources
        for ds in datasets:
            ds.close()
        
        # Define the output file path
        output_path = os.path.join(output_dir, f"{city_folder}_ERA_RH_total.nc")
        
        # Save the combined dataset to the output file
        combined_dataset.to_netcdf(output_path)
        print(f"Processed and saved: {output_path}")

print("Processing completed.")
