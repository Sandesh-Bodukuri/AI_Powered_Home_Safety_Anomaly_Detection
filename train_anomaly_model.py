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