from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    try:
        data = pd.read_csv('indoor_data_with_anomalies.csv')
        # Convert timestamp to string for easier handling in JavaScript
        data['timestamp'] = data['timestamp'].astype(str)
        # Get the last 500 data points (adjust as needed)
        recent_data = data.tail(500).to_dict(orient='records')
        return render_template('index.html', sensor_data=recent_data)
    except FileNotFoundError:
        return "Error: indoor_data_with_anomalies.csv not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)