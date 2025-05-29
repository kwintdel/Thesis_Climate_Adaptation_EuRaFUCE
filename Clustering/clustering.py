import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler

# File paths
model_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/knn_classifier_model.pkl'
scaler_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/scaler_model.pkl'
new_data_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/new_combined.csv'
train_data_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/train_combined.csv'
output_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/new_classified.csv'

# Load the trained KNN model and scaler
knn = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Load the new data
new_data = pd.read_csv(new_data_path)

# Load the train data to get the feature column order (excluding 'City' and 'Cluster')
train_data = pd.read_csv(train_data_path)
expected_feature_columns = train_data.drop(columns=['City', 'Cluster']).columns

# Ensure the new data has the correct column order
features = new_data[expected_feature_columns]

# Save the 'City' column for later use
city_column = new_data['City']

# Scale the features using MinMaxScaler (same scaling method as during training)
#scaler = MinMaxScaler()
features_scaled = scaler.transform(features)   # Use fit_transform because new data must be scaled independently

# Classify the data using the loaded KNN model
predicted_clusters = knn.predict(features_scaled)

# Add the predictions as a new column
new_data['Cluster'] = predicted_clusters

# Save the classified data to a new CSV file
new_data.to_csv(output_path, index=False)

print(f"Classified data saved to {output_path}")
