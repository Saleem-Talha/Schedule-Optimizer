import mysql.connector
import requests

def get_user_schedule(user_email):
    """
    Fetch the schedule data for the given user email from the database.
    """
    try:
        # Connect to your MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='talha_db'
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch schedule for the given user email
        query = "SELECT * FROM schedules WHERE user_id = %s"
        cursor.execute(query, (user_email,))
        schedule_data = cursor.fetchall()

        return schedule_data

    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def optimize_schedule(api_key, schedule_data):
    """
    Use the Gemini API to suggest an optimal schedule.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    # Prepare the payload as per Gemini API requirements
    payload = {
        "prompt": {
            "text": f"Optimize this schedule: {schedule_data}"
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP status
        return response.json()  # Assuming the API returns a JSON response

    except requests.RequestException as e:
        print(f"Error interacting with Gemini API: {e}")
        return None

def main(user_email, api_key):
    """
    Main function to fetch user schedule and optimize it using the Gemini API.
    """
    # Fetch the user's schedule
    schedule_data = get_user_schedule(user_email)

    if not schedule_data:
        print("No schedule found for the provided email.")
        return

    # Get the optimized schedule from the Gemini API
    optimized_schedule = optimize_schedule(api_key, schedule_data)

    if optimized_schedule:
        print("Optimized Schedule:")
        print(optimized_schedule)  # Replace with more user-friendly output
    else:
        print("Failed to retrieve optimized schedule.")

# Example usage
if __name__ == "__main__":
    user_email = "saleemtalha967@gmail.com"  # Input email
    api_key = "AIzaSyBeUAGckwfwpB2La5uQ1-rpIlaL4tRUA7Y"  # Input Gemini API key
    main(user_email, api_key)
