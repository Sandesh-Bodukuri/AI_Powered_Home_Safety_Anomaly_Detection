import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load the simulated data from a CSV file
normal_data = pd.read_csv('c:/Users/0913S/OneDrive/Documents/Project-0/indoor_data_with_anomalies.csv')

# Validate required columns
required_columns = ['temperature', 'humidity', 'light', 'label']
if not all(col in normal_data.columns for col in required_columns):
    raise ValueError(f"The dataset must contain the following columns: {required_columns}")

# Separate features (X) and labels (y)
X = normal_data[['temperature', 'humidity', 'light']]
y = normal_data['label']

# Identify normal data points for training
normal_indices = y[y == 0].index
normal_data_X = X.loc[normal_indices]

# Split normal data into training and validation sets
X_train, X_val = train_test_split(normal_data_X, test_size=0.2, random_state=42)

# For testing, we'll use all the data (both normal and anomalous)
X_test = X
y_test = y

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Shape of X_train (Normal Data for Training):", X_train.shape)
print("Shape of X_val (Validation Data):", X_val.shape)
print("Shape of X_test (All Data for Testing):", X_test.shape)
print("Shape of y_test (Labels for All Data):", y_test.shape)
print("\nFirst few rows of X_train:")
print(X_train.head())
print("\nFirst few rows of X_val:")
print(X_val.head())
print("\nFirst few rows of X_test:")
print(X_test.head())
print("\nFirst few rows of y_test:")
print(y_test.head())

from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report, confusion_matrix

# Train the One-Class SVM model
ocsvm = OneClassSVM(kernel='rbf', gamma='auto', nu=0.01)  
ocsvm.fit(X_train_scaled)

# Predict on the test set
y_pred = ocsvm.predict(X_test_scaled)

# Convert predictions to match the labels (1 for anomaly, 0 for normal)
y_pred = [0 if pred == 1 else 1 for pred in y_pred]  # One-Class SVM outputs 1 for inliers and -1 for outliers

# Evaluate the model
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))


from sklearn.ensemble import IsolationForest

# Train the Isolation Forest model
iso_forest = IsolationForest(n_estimators=200, contamination=0.06, random_state=42)  
iso_forest.fit(X_train_scaled)

# Predict on the test set
y_pred_iso = iso_forest.predict(X_test_scaled)

# Convert predictions to match the labels (1 for anomaly, 0 for normal)
y_pred_iso = [0 if pred == 1 else 1 for pred in y_pred_iso]  # Isolation Forest outputs 1 for inliers and -1 for outliers

# Evaluate the model
print("\nConfusion Matrix (Isolation Forest):")
print(confusion_matrix(y_test, y_pred_iso))

print("\nClassification Report (Isolation Forest):")
print(classification_report(y_test, y_pred_iso, target_names=['Normal', 'Anomaly']))