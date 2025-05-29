import numpy as np
import pandas as pd
import dask.dataframe as dd

# Load data with Dask
cities = dd.read_csv('/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/city characteristics/all_data_FINAL.csv', blocksize=50e6)

# Select relevant columns, excluding 'city'
cities_selected = cities[['HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP', 'T_TARGET', 'wind_speed', 'TCC', 'BLH', 'SSR', 'SOLAR_ELEV', 'DECL']]

# Dictionary to store computed statistics for each column
statistics = {}

# Compute each statistic separately
statistics['mean'] = cities_selected.mean().compute()
statistics['std'] = cities_selected.std().compute()
statistics['min'] = cities_selected.min().compute()
statistics['max'] = cities_selected.max().compute()
statistics['25%'] = cities_selected.quantile(0.25).compute()
statistics['75%'] = cities_selected.quantile(0.75).compute()

# Combine statistics into a single DataFrame
combined_df = pd.DataFrame(statistics)

# Set the index name for clarity
combined_df.index.name = 'Variable'

# Save the result to CSV
combined_df.to_csv('/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/city_char/city_char_results/overall_statistics.csv')
