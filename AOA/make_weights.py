import numpy as np
import joblib
import sklearn
import pandas as pd



model_CL1=joblib.load("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/models/model_ALLcities_CL1.joblib")
model_CL2=joblib.load("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/models/model_ALLcities_CL2.joblib")
model_CL3=joblib.load("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/models/model_ALLcities_CL3.joblib")
model_15cities=joblib.load("/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/models/GENERAL_15cities.joblib")

importances_CL1 = model_CL1.feature_importances_
importances_CL2 = model_CL2.feature_importances_
importances_CL3 = model_CL3.feature_importances_
importances_15cities = model_15cities.feature_importances_
std_CL1 = np.std([tree.feature_importances_ for tree in model_CL1.estimators_], axis=0)
std_CL2 = np.std([tree.feature_importances_ for tree in model_CL2.estimators_], axis=0)
std_CL3 = np.std([tree.feature_importances_ for tree in model_CL3.estimators_], axis=0)
std_15cities = np.std([tree.feature_importances_ for tree in model_15cities.estimators_], axis=0)

names = ['LC_CORINE', 'IMPERV', 'HEIGHT', 'COAST', 'ELEV', 'POP', 'RH', 'SP', 'PRECIP','T_2M', 'wind_speed', 'TCC',  'CAPE', 'BLH', 'SSR','SOLAR_ELEV', 'DECL']

# Combine names with importances 
def save_importances(names, importances, std, filename):
    df = pd.DataFrame({
        "Feature": names,
        "Importance": importances,
        "Std":std,
    })
    df.to_csv(filename, index=False)

save_importances(names, importances_CL1, std_CL1, "../AOA_data/importances_CL1.csv")
save_importances(names, importances_CL2, std_CL2, "../AOA_data/importances_CL2.csv")
save_importances(names, importances_CL3, std_CL3,"../AOA_data/importances_CL3.csv")
save_importances(names, importances_15cities, std_15cities, "../AOA_data/importances_15cities.csv")