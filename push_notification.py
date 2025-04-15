import requests
import os
import pickle
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def send_pushover_notification(user_key, api_token, title, message):
    """
    Sends a push notification via Pushover.

    Args:
        user_key (str): Your Pushover User Key.
        api_token (str): Your Pushover API Token/Key for the application.
        title (str): The title of the notification (optional).
        message (str): The main message body of the notification.

    Returns:
        bool: True if the notification was sent successfully, False otherwise.
    """
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": api_token,
        "user": user_key,
        "message": message,
    }
    if title:
        data["title"] = title

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending Pushover notification: {e}")
        if response is not None:
            print("Response Content:", response.text)  # Print the response content for more details
        return False

if __name__ == '__main__':
    # Load sensitive information from environment variables
    PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
    PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        print("Error: Missing Pushover User Key or API Token in environment variables.")
        exit()

    # Load the trained anomaly detection model and scaler
    try:
        with open('anomaly_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        print("Model loaded successfully.")

        with open('scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        print("Scaler loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the model and scaler files are in the correct directory.")
        exit()
    except pickle.UnpicklingError as e:
        print(f"Error loading pickle file: {e}")
        print("The model or scaler file might be corrupted. Please recreate them.")
        exit()

    # Verify the loaded objects
    print(f"Loaded model type: {type(loaded_model)}")
    print(f"Loaded scaler type: {type(scaler)}")

    # Simulate new data and trigger notifications
    try:
        # Load the dataset with injected anomalies
        anomaly_data = pd.read_csv('indoor_data_with_anomalies.csv')
        print("Anomaly Data loaded successfully.")
        print("Shape of Anomaly Data:", anomaly_data.shape)

        # Filter rows with label == 1 (anomalies) and get the last 5
        simulated_data = anomaly_data[anomaly_data['label'] == 1].tail(5)
        if simulated_data.empty:
            print("No anomalous data points found to simulate.")
        else:
            simulated_features = simulated_data[['temperature', 'humidity', 'light']]
            print("Simulated data loaded successfully.")
            print("Shape of Simulated Features:", simulated_features.shape)

            # Scale the simulated data
            simulated_features_scaled = scaler.transform(simulated_features)

            # Predict anomalies
            predictions = loaded_model.predict(simulated_features_scaled)

            # Trigger notifications for anomalies with details
            for i, prediction in enumerate(predictions):
                if prediction == -1:  # -1 indicates an anomaly
                    title = "Anomaly Detected!"
                    timestamp_str = simulated_data.iloc[i]['timestamp']
                    temperature = simulated_data.iloc[i]['temperature']
                    humidity = simulated_data.iloc[i]['humidity']
                    light = simulated_data.iloc[i]['light']
                    message = f"Timestamp: {timestamp_str}\nTemperature: {temperature:.2f}°C\nHumidity: {humidity:.2f}%\nLight: {light} lux"
                    if send_pushover_notification(PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN, title, message):
                        print(f"Notification sent for anomaly at {timestamp_str}")
                    else:
                        print(f"Failed to send notification for anomaly at {timestamp_str}")
                else:
                    timestamp_str = simulated_data.iloc[i]['timestamp']
                    print(f"Data at {timestamp_str} predicted as normal (label was 1).") # This should ideally not happen if we filtered correctly
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the 'indoor_data_with_anomalies.csv' file is in the correct directory.")
    except Exception as e:
        print(f"An unexpected error occurred during simulation and notification: {e}")