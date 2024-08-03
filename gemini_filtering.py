import google.generativeai as gai
import json
import os

gai.configure(api_key="AIzaSyDk8M6rDC1P8sKl6G1sS3CWjGOQLRWzPiE")
model = gai.GenerativeModel('gemini-1.0-pro-latest')
user_preferences = ["food", "bar"] # -> these are jsut examples that will be variable based on what the user selects on the frontend 


with open('places_nearby.json', 'r') as file:
    places_data = json.load(file)

prompt = f"""
Given the following JSON data of places:
{json.dumps(places_data, indent=2)}

Filter the places based on these user preferences: {user_preferences}
Return only the filtered places as a valid JSON array.
"""

response = model.generate_content(prompt)
filtered_places = json.loads(response.text)
with open('filtered_places.json', 'w') as outfile:
    json.dump(filtered_places, outfile, indent=2)
