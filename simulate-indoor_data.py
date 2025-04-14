import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define start and end times
start_time = datetime(2025, 4, 12, 21, 24, 0)  # Starting time
end_time = start_time + timedelta(hours=24)  # 24 hours later

# Generate timestamps at 5-minute intervals
timestamps = pd.date_range(start=start_time, end=end_time, freq='5 min', inclusive='left')  # Exclude the last timestamp to ensure 288 points
timestamps_list = timestamps.tolist()

# Define ranges for temperature, humidity, and light
normal_temp_range = (24, 37)
normal_humidity_range = (30, 60)
normal_light_day_range = (300, 800)
normal_light_night_range = (50, 150)

# Define typical day/night hours 
day_start_hour = 6
day_end_hour = 18

# Generate temperature data
num_points = len(timestamps)
temp_mean = np.mean(normal_temp_range)
temperature = np.random.normal(loc=temp_mean, scale=1.5, size=num_points)
temperature = np.clip(temperature, normal_temp_range[0], normal_temp_range[1])  # Ensure values stay within the normal range

# Generate humidity data
humidity_mean = np.mean(normal_humidity_range)
humidity = np.random.normal(loc=humidity_mean, scale=5, size=num_points)
humidity = np.clip(humidity, normal_humidity_range[0], normal_humidity_range[1])  # Ensure values stay within the normal range

# Generate light data
light = []
for ts in timestamps:
    hour = ts.hour
    if day_start_hour <= hour < day_end_hour:
        light_value = np.random.randint(normal_light_day_range[0], normal_light_day_range[1] + 1)
    else:
        light_value = np.random.randint(normal_light_night_range[0], normal_light_night_range[1] + 1)
    light.append(light_value)
light = np.array(light)

# Create DataFrame
normal_data = pd.DataFrame({
    'timestamp': timestamps,
    'temperature': temperature,
    'humidity': humidity,
    'light': light
})
normal_data['label'] = 0  # Normal data label

# Print the first few rows of the DataFrame
print(normal_data.head())
print(f"Total data points generated: {len(normal_data)}")
# Save the normal data to a CSV file
normal_data.to_csv('normal_data.csv', index=False)


# --- Anomaly Injection Logic Below ---

# Define time interval
time_interval = timedelta(minutes=5)

# 1. Rapid Increase in Humidity (Water Leak Simulation)
anomaly_time_start_humidity = datetime(2025, 4, 13, 9, 0, 0)
anomaly_duration_humidity = timedelta(minutes=15)
num_steps_humidity = int(anomaly_duration_humidity / time_interval) + 1

if not normal_data[normal_data['timestamp'] >= anomaly_time_start_humidity].empty:
    start_index_humidity = normal_data.index[normal_data['timestamp'] >= anomaly_time_start_humidity][0]
    indices_humidity = range(start_index_humidity, start_index_humidity + num_steps_humidity)

    normal_humidity_at_start = normal_data.loc[start_index_humidity, 'humidity']
    humidity_increase_values = np.linspace(normal_humidity_at_start, 95, len(indices_humidity))
    normal_data.loc[indices_humidity, 'humidity'] = humidity_increase_values
    normal_data.loc[indices_humidity, 'label'] = 1
else:
    print(f"Warning: No matching timestamp found for {anomaly_time_start_humidity}")

# 2. Sustained Low Temperature (AC Malfunction Simulation)
anomaly_time_start_temp = datetime(2025, 4, 13, 15, 0, 0)
anomaly_duration_temp_ramp = timedelta(minutes=30)
num_steps_temp_ramp = int(anomaly_duration_temp_ramp / time_interval) + 1
anomaly_duration_temp_sustain = timedelta(hours=2)
num_steps_temp_sustain = int(anomaly_duration_temp_sustain / time_interval)

if not normal_data[normal_data['timestamp'] >= anomaly_time_start_temp].empty:
    start_index_temp = normal_data.index[normal_data['timestamp'] >= anomaly_time_start_temp][0]
    indices_temp_ramp = range(start_index_temp, start_index_temp + num_steps_temp_ramp)
    indices_temp_sustain = range(start_index_temp + num_steps_temp_ramp, start_index_temp + num_steps_temp_ramp + num_steps_temp_sustain)

    normal_temp_at_start = normal_data.loc[start_index_temp, 'temperature']
    temp_decrease_values = np.linspace(normal_temp_at_start, 18, len(indices_temp_ramp))
    normal_data.loc[indices_temp_ramp, 'temperature'] = temp_decrease_values
    normal_data.loc[indices_temp_ramp, 'label'] = 1
    normal_data.loc[indices_temp_sustain, 'temperature'] = 18
    normal_data.loc[indices_temp_sustain, 'label'] = 1
else:
    print(f"Warning: No matching timestamp found for {anomaly_time_start_temp}")

# 3. Unexpected Fluctuations in Illumination (Faulty Wiring Simulation at Night)
anomaly_times_light = [
    datetime(2025, 4, 13, 19, 4, 0),  
    datetime(2025, 4, 13, 20, 34, 0),  
    datetime(2025, 4, 13, 21, 14, 0)
]

for anomaly_time in anomaly_times_light:
    try:
        # Find the index of the anomaly timestamp
        index_light = normal_data.index[normal_data['timestamp'] == anomaly_time][0]
        
        # Introduce a flicker pattern over 5 consecutive timestamps
        flicker_pattern = [5, 700, 10, 650, 15]  # Alternating low and high values for nighttime
        for i, flicker_value in enumerate(flicker_pattern):
            if index_light + i < len(normal_data):  # Ensure we don't go out of bounds
                normal_data.loc[index_light + i, 'light'] = flicker_value
                normal_data.loc[index_light + i, 'label'] = 1  # Mark as anomaly
    except IndexError:
        print(f"Warning: Timestamp {anomaly_time} not found in the generated data.")


# --- Inspection of the Modified DataFrame ---
print("\n--- Modified DataFrame Head and Tail ---")
print(normal_data.head())
print(normal_data.tail())

print("\n--- Label Value Counts ---")
print(normal_data['label'].value_counts())

# --- Optional: Plotting for Visual Inspection ---
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(normal_data['timestamp'], normal_data['temperature'], label='Temperature')
plt.scatter(normal_data[normal_data['label'] == 1]['timestamp'], normal_data[normal_data['label'] == 1]['temperature'], color='red', marker='o', label='Temperature Anomaly')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Temperature with Anomalies')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(normal_data['timestamp'], normal_data['humidity'], label='Humidity')
plt.scatter(normal_data[normal_data['label'] == 1]['timestamp'], normal_data[normal_data['label'] == 1]['humidity'], color='green', marker='o', label='Humidity Anomaly')
plt.xlabel('Timestamp')
plt.ylabel('Humidity (%)')
plt.title('Humidity with Anomalies')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(normal_data['timestamp'], normal_data['light'], label='Light')
plt.scatter(normal_data[normal_data['label'] == 1]['timestamp'], normal_data[normal_data['label'] == 1]['light'], color='purple', marker='o', label='Light Anomaly')
plt.xlabel('Timestamp')
plt.ylabel('Light Level')
plt.title('Light with Anomalies')
plt.legend()
plt.grid(True)
plt.show()
# Save the modified DataFrame with anomalies to a new CSV file
normal_data.to_csv('indoor_data_with_anomalies.csv', index=False)

print("CSV file with anomalies has been saved as 'indoor_data_with_anomalies.csv'.")