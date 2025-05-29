import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
#TRIED WITH CROSS VAL, BUT WAS WORSE



# Define the file path
file_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/train_combined.csv'
new_data_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/new_combined.csv'

# Load the dataset
data = pd.read_csv(file_path)
data_new = pd.read_csv(new_data_path)
data_big = pd.concat([data.drop(columns = ['Cluster']), data_new]) #use the complete available data to scale
# Drop the 'City' column as it is not a feature
features = data.drop(columns=['City', 'Cluster'])
features_big = data_big.drop(columns = ['City'])

# Extract the target column
target = data['Cluster']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)

# Scale the features using MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(features_big)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Extract and document the min and max values for each feature
scaling_info = pd.DataFrame({'Feature': features.columns, 
                             'Min': scaler.data_min_, 
                             'Max': scaler.data_max_})

# Save scaling information for reference
scaling_info.to_csv("../cluster_results/scaling_info.csv", index=False)

# Create and train the KNN classifier
knn = KNeighborsClassifier(n_neighbors=1)  
knn.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = knn.predict(X_test_scaled)

# Evaluate the model
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model for future use
output_model_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/knn_classifier_model.pkl'
output_scaler_path = '/data/gent/vo/000/gvo00041/Kwint_personal/UrbClim_Emulator/ownscripts/clustering/cluster_results/scaler_model.pkl'
joblib.dump(scaler, output_scaler_path)
joblib.dump(knn, output_model_path)
print(f"Trained KNN model saved to {output_model_path}")
