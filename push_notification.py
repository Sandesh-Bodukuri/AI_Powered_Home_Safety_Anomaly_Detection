import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def send_onesignal_notification(app_id, rest_api_key, heading, content):
    """
    Sends a push notification via OneSignal.

    Args:
        app_id (str): Your OneSignal App ID.
        rest_api_key (str): Your OneSignal REST API Key.
        heading (str): The title of the notification.
        content (str): The main message body of the notification.

    Returns:
        bool: True if the notification was sent successfully, False otherwise.
    """
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {rest_api_key}"
    }
    payload = {
        "app_id": app_id,
        "contents": {"en": content},  # 'en' for English
        "headings": {"en": heading},
        "included_segments": ["Subscribed Users"]  # Send to all subscribed users
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending OneSignal notification: {e}")
        return False

if __name__ == '__main__':
    # Load sensitive information from environment variables
    YOUR_APP_ID = os.getenv("ONESIGNAL_APP_ID")
    YOUR_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY")

    if not YOUR_APP_ID or not YOUR_REST_API_KEY:
        print("Error: Missing OneSignal App ID or REST API Key in environment variables.")
    else:
        # Example usage:
        notification_heading = "Test Alert!"
        notification_content = "This is a test notification from our anomaly detection system."

        if send_onesignal_notification(YOUR_APP_ID, YOUR_REST_API_KEY, notification_heading, notification_content):
            print("Test notification sent successfully!")
        else:
            print("Failed to send test notification.")