import requests
import os
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
    else:
        # Example usage:
        notification_title = "Anomaly Detected!"
        notification_message = "Our system has detected an unusual sensor reading. Please check the logs."

        if send_pushover_notification(PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN, notification_title, notification_message):
            print("Pushover notification sent successfully!")
        else:
            print("Failed to send Pushover notification.")