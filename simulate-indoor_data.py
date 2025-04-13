import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define start and end times
start_time = datetime(2025, 4, 12, 21, 24, 0)  # Starting time
end_time = start_time + timedelta(hours=24)  # 24 hours later

# Generate timestamps at 5-minute intervals
timestamps = pd.date_range(start=start_time, end=end_time, freq='5 min', inclusive='left')  # Exclude the last point
timestamps_list = timestamps.tolist()

# Define ranges for temperature, humidity, and light
normal_temp_range = (24, 37)
normal_humidity_range = (30, 60)
normal_light_day_range = (300, 800)
normal_light_night_range = (50, 150)

# Define typical day/night hours (adjust as needed for Hyderabad)
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
normal_data.to_csv('indoor_data.csv', index=False)