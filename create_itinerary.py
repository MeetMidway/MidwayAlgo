import google.generativeai as gai
import json
import os
import time
from dotenv import load_dotenv
from google.api_core.exceptions import InternalServerError

load_dotenv()
gemini_api_key = ""

gai.configure(api_key=gemini_api_key)
model = gai.GenerativeModel('gemini-1.5-pro-latest')

def generate_itinerary():
    # Load the filtered places data
    with open('filtered_places.json', 'r') as file:
        filtered_places = json.load(file)

    # Construct the prompt for Gemini to create an itinerary
    itinerary_prompt = f"""
    You are an AI assistant that creates an optimized itinerary for a fun and diverse trip based on the following places. Each place has a rating and a priority tag. The goal is to pick out the 4 best places for a well-rounded trip, ensuring a good balance of activities and preferences. Here is the list of places in JSON format:

    {json.dumps(filtered_places, indent=2)}

    Please use both the ratings and priority tags to select the 4 best places. Ensure the itinerary makes sense and provides a good variety of activities. For example, do not include only food places. Try to include most of the user preferences, but if it's not possible, prioritize variety and overall experience. Make sure the final output is a valid JSON array.
    """

    # Debugging: Print the constructed itinerary prompt
    print("Constructed Itinerary Prompt:\n", itinerary_prompt)

    # Send the itinerary request to Gemini API with retry logic
    itinerary_response = _retry_api_call(model.generate_content, itinerary_prompt)

    # Debugging: Print the itinerary response text
    print("Itinerary Response text:", itinerary_response.text)

    # Ensure itinerary response is not empty and is valid JSON
    if not itinerary_response.text.strip():
        raise ValueError("Received empty response from Gemini API")

    # Attempt to clean and parse the itinerary response text as JSON
    try:
        cleaned_itinerary_response_text = itinerary_response.text.strip()
        
        # Remove leading and trailing backticks and json markdown
        if cleaned_itinerary_response_text.startswith("```json"):
            cleaned_itinerary_response_text = cleaned_itinerary_response_text[7:]
        if cleaned_itinerary_response_text.endswith("```"):
            cleaned_itinerary_response_text = cleaned_itinerary_response_text[:-3]

        # Validate and parse JSON
        generated_itinerary = json.loads(cleaned_itinerary_response_text)
        print("Generated itinerary:", generated_itinerary)

        # Ensure the generated itinerary is an array with exactly 4 items
        if not isinstance(generated_itinerary, list) or len(generated_itinerary) != 4:
            raise ValueError("Generated itinerary is not a valid list with exactly 4 items.")
        
    except (json.JSONDecodeError, ValueError) as e:
        print("Failed to decode JSON itinerary response:", e)
        print("Cleaned Itinerary Response text:", cleaned_itinerary_response_text)
        generated_itinerary = []

    # Save the generated itinerary to a JSON file if they are valid
    if generated_itinerary:
        with open('generated_itinerary.json', 'w') as outfile:
            json.dump(generated_itinerary, outfile, indent=2)
        print("Generated itinerary saved to 'generated_itinerary.json'.")
    else:
        print("No valid generated itinerary found in the response.")

def _retry_api_call(api_call, *args, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return api_call(*args)
        except InternalServerError as e:
            print(f"InternalServerError encountered: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise RuntimeError("Failed to get a valid response from the Gemini API after multiple attempts")

if __name__ == "__main__":
    generate_itinerary()