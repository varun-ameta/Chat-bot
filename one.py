import openai
import requests
import datetime
from secreatkey import openapi_key, weather_api_key

openai.api_key = openapi_key
weather_api_key=weather_api_key

# Create a dictionary to store chat histories for each email
email_chat_histories = {}
# Create a dictionary to store suggestions count for each email
email_suggestions_count = {}

# Function to display weather information
def display_weather_info(city, temperature, description, time):
    print(f'Weather information for {city} as of {time}:')
    print(f'Temperature: {temperature} K')
    print(f'Condition: {description.capitalize()}')

def city(location):
    city = location
    get_weather_data(city)

# Replace with your OpenWeatherMap API key
api_key = weather_api_key

# Global variables
temperature = None
description = None
time = None

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city):
    global temperature, description, time  # Access the global variables
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(base_url)
    data = response.json()

    # Assign values to the global variables
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data

def generate_response(chat_history, user_input):
    # Combine the chat history with the user's new input
    new_message = {"role": "user", "content": user_input}
    chat_history.append(new_message)

    # Generate a response based on the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        max_tokens=250,
        stop=None
    )

    # Extract and return the chatbot's response
    bot_response = response.choices[0].message["content"]
    return bot_response

def main():
    global email_chat_histories, email_suggestions_count  # Access the global dictionaries

    print("Chatbot: Hello! I'm here to suggest activities when you're bored.")

    while True:
        # Get the user's email (you can change this to get it from user input)
        email = input('Chatbot: Please provide your Email I\'d (type "exit" to quit):\nYou: ')
        if email == "exit":
            break

        # Initialize a chat history for the email if not already exists
        if email not in email_chat_histories:
            email_chat_histories[email] = []

        chat_history = email_chat_histories[email]  # Get the chat history

        # Initialize the suggestions count for the email if not already exists
        if email not in email_suggestions_count:
            email_suggestions_count[email] = 0

        # Reset the suggestions count if it exceeds 3
        if email_suggestions_count[email] >= 3:
            email_suggestions_count[email] = 0
            print("Chatbot: You've received the maximum number of suggestions (3 times).")

        # Define a list of questions to ask the user
        questions = [
            "Are you bored?",
            "What is your good name?",
            "What do you love to do in your free time?",
            "Do you prefer indoor or outdoor activities?",
            "Where are you from?",
            "How many people are with you currently?",
        ]

        user_responses = []  # Initialize a list to store user responses

        for question in questions:
            user_response = input(f'Chatbot: {question}\nYou: ')
            chat_history.append({"role": "user", "content": user_response})
            user_responses.append(user_response)

            # Stop if the user responds "No" to the first question
            if question == "Are you bored?" and user_response.lower() == "no":
                print("Chatbot: Okay, have a great day!")
                return

        # Suggest an activity based on the user's responses to the questions
        suggest_activity(chat_history, user_responses, email)

# Global Variable
location = None
def suggest_activity(chat_history, user_responses, email):
    # Customize the activity suggestion based on the user's responses to the predefined questions
    boredom = user_responses[0].lower()
    name = user_responses[1].lower()
    free_time_activity = user_responses[2].lower()
    indoor_or_outdoor = user_responses[3].lower()
    location = user_responses[4].lower()
    people_with_you = user_responses[5].lower()
    weather_details = get_weather_data(location)
    
    # Check if the user has already received 3 suggestions
    if email_suggestions_count[email] < 3:
        print("Chatbot: Searching for activity suggestions...")
        suggestion = generate_suggestion(boredom, name, free_time_activity, weather_details, indoor_or_outdoor, location, people_with_you)
        print(f"Chatbot: Based on your responses and {time}, {temperature}K, {description}, I suggest: {suggestion}")

        # Increase the suggestions count for this email
        email_suggestions_count[email] += 1
    else:
        print("Chatbot: You've received the maximum number of suggestions (3 times).")

def generate_suggestion(boredom, name, free_time_activity, weather_details, indoor_or_outdoor, location, people_with_you):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides activity suggestions."},
            {"role": "user", "content": f"I am bored: {boredom}"},
            {"role": "user", "content": f"My good name is: {name}"},
            {"role": "user", "content": f"I love to do in my free time: {free_time_activity}"},
            {"role": "user", "content": f"The outside is: {weather_details}"},
            {"role": "user", "content": f"I prefer indoor or outdoor activities: {indoor_or_outdoor}"},
            {"role": "user", "content": f"I am from: {location}"},
            {"role": "user", "content": f"I am with {people_with_you} people currently."},
        ],
        max_tokens=250
    )

    return response.choices[0].message["content"]

if __name__ == '__main__':
    main()




















