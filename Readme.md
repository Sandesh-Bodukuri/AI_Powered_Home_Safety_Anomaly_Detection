# Home Sensor Dashboard

This project is a web-based dashboard that visualizes simulated indoor environmental data (temperature, humidity, and light levels) and highlights anomalies using a trained machine learning model and predefined timestamps. It also features integration with the Pushover API for real-time anomaly alerts.

## Overview

The main purpose of this project is to provide an intuitive interface for monitoring indoor conditions and quickly identifying unusual patterns that could indicate potential issues related to comfort, health, or energy efficiency in a home environment.

Key features include:

* **Data Visualization:** Interactive line graphs displaying simulated temperature, humidity, and light levels over time.
* **General Anomaly Detection:** Identification of anomalies using a trained machine learning model (indicated by green circles on the graphs).
* **Specific Anomaly Highlighting:** Highlighting of anomalies at predefined timestamps for targeted analysis (indicated by red circles on the graphs).
* **Push Notifications:** Integration with the Pushover API to send real-time alerts to user devices when anomalies are detected (requires user configuration with their Pushover credentials).
* **Simulated Data:** Utilizes a CSV file (`indoor_data_with_anomalies.csv`) containing simulated indoor sensor data for demonstration purposes.

## Setup and Running the Application

1.  **Prerequisites:**
    * Python 3.6 or higher installed on your system.
    * pip (Python package installer) should be included with your Python installation.

2.  **Installation:**
    * Clone or download the project repository to your local machine.
    * Navigate to the project's root directory in your terminal or command prompt.
    * Install the required Python libraries using pip:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Data File:**
    * Ensure that the `indoor_data_with_anomalies.csv` file is located in the same directory as the `dashboard.py` file.

4.  **Running the Dashboard:**
    * In your terminal or command prompt (still in the project directory), run the Flask application:
        ```bash
        python dashboard.py
        ```
    * Open your web browser and go to the address `http://127.0.0.1:5000/` to view the dashboard.

## Project Components

* `dashboard.py`: The main Flask application file containing the backend logic for data loading, visualization, anomaly detection integration, and Pushover notifications.
* `templates/index.html`: The HTML template for rendering the web dashboard.
* `indoor_data_with_anomalies.csv`: The CSV file containing the simulated sensor data.
* `requirements.txt`: A list of Python libraries required to run the application.


## Anomaly Detection

* General anomalies are detected using a trained **One-Class SVM** machine learning model. The model is integrated into the `dashboard.py` script and identifies data points that deviate significantly from the normal patterns in the simulated data.
* Specific anomalies at predefined timestamps are highlighted based on hardcoded timestamps within the `dashboard.py` for demonstration and targeted analysis.

## Push Notifications (Pushover)

* The application includes functionality to send push notifications via the Pushover API when anomalies are detected.
* **Note:** To receive these notifications on a personal device, a user needs to:
    * Install the Pushover app (iOS or Android).
    * Create a Pushover account and obtain their user key.
    * Integrate their Pushover user key into the configuration of the `dashboard.py` file (you might have a placeholder or instructions within the code for this).

## Future Enhancements

Potential future developments for this project include:

* Integrating with real-time data streams from actual indoor sensors.
* Implementing more advanced anomaly detection models and forecasting techniques.
* Adding user customization for alert thresholds and notification preferences.
* Expanding support for a wider range of sensors (e.g., air quality, motion).
* Integrating with other smart home platforms.
* Exploring more advanced data visualization and interactive elements.

## Author

Sandesh-Bodukuri

