import google.generativeai as gai
import json
import os

gai.configure(api_key="PUT KEY HERE ILL FIGURE OUT THE ENV FILE LATER")
model = gai.GenerativeModel('gemini-1.5-pro-latest')

# Collect user preferences
user_preferences = []
print("Please enter your preferences from highest ranked to lowest ranked:")

for i in range(4):
    preference = input(f"Enter preference {i+1}: ")
    user_preferences.append(preference)

# Rank user preferences
ranked_preferences = sorted(user_preferences, key=lambda x: user_preferences.index(x))

# Load the places data
with open('places_nearby.json', 'r') as file:
    places_data = json.load(file)

# Construct the prompt for Gemini to filter and prioritize places
filter_prompt = f"""
You are an AI assistant that filters and prioritizes places based on user preferences but skips the preference if no places match it. Here is a list of places in JSON format:

{json.dumps(places_data, indent=2)}

The user preferences are ranked in the following order (highest to lowest priority): {ranked_preferences}.

Please filter and prioritize the places based on these preferences and return the filtered list in JSON format. Ensure that the places are not too standard, as you are an assistant designed to help a user organize a fun trip of exploration. For example, do not return a grocery store, even though food was one of the tags. 

IMPORTANT: You are an assistant that does NOT need to fulfill every single user preference if unable to. If none exist within a certain preference, don't filter it. Just do your best to get most of them.
"""

# Debugging: Print the constructed filter prompt
print("Constructed Filter Prompt:\n", filter_prompt)

# Send the filter request to Gemini API
filter_response = model.generate_content(filter_prompt)

# Debugging: Print the filter response text
print("Filter Response text:", filter_response.text)

# Ensure filter response is not empty and is valid JSON
if not filter_response.text.strip():
    raise ValueError("Received empty response from Gemini API")

# Attempt to clean and parse the filter response text as JSON
try:
    cleaned_filter_response_text = filter_response.text.strip()
    
    # Remove leading and trailing backticks and json markdown
    if cleaned_filter_response_text.startswith("```json"):
        cleaned_filter_response_text = cleaned_filter_response_text[7:]
    if cleaned_filter_response_text.endswith("```"):
        cleaned_filter_response_text = cleaned_filter_response_text[:-3]

    filtered_places = json.loads(cleaned_filter_response_text)
    print("Filtered places:", filtered_places)
except json.JSONDecodeError as e:
    print("Failed to decode JSON filter response:", e)
    print("Cleaned Filter Response text:", cleaned_filter_response_text)
    filtered_places = []

# Proceed to add priority tags if filtered_places is valid
if filtered_places:
    # Construct the prompt for Gemini to add priority tags
    priority_prompt = f"""
    You are an AI assistant that enhances a list of filtered places by adding a "priority" tag. Here is a list of places in JSON format:

    {json.dumps(filtered_places, indent=2)}

    The user preferences are ranked in the following order (highest to lowest priority): {ranked_preferences}.

    Please add a "priority" tag with values "high", "medium", or "low" to each place based on how well it matches the preferences.
    """

    # Debugging: Print the constructed priority prompt
    print("Constructed Priority Prompt:\n", priority_prompt)

    # Send the priority request to Gemini API
    priority_response = model.generate_content(priority_prompt)

    # Debugging: Print the priority response text
    print("Priority Response text:", priority_response.text)

    # Ensure priority response is not empty and is valid JSON
    if not priority_response.text.strip():
        raise ValueError("Received empty response from Gemini API")

    # Attempt to clean and parse the priority response text as JSON
    try:
        cleaned_priority_response_text = priority_response.text.strip()
        
        # Remove leading and trailing backticks and json markdown
        if cleaned_priority_response_text.startswith("```json"):
            cleaned_priority_response_text = cleaned_priority_response_text[7:]
        if cleaned_priority_response_text.endswith("```"):
            cleaned_priority_response_text = cleaned_priority_response_text[:-3]

        places_with_priority = json.loads(cleaned_priority_response_text)
        print("Places with priority:", places_with_priority)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON priority response:", e)
        print("Cleaned Priority Response text:", cleaned_priority_response_text)
        places_with_priority = []

    # Save the places with priority to the same JSON file if they are valid
    if places_with_priority:
        with open('filtered_places.json', 'w') as outfile:
            json.dump(places_with_priority, outfile, indent=2)
        print("Filtered places with priority based on user preferences saved to 'filtered_places.json'.")
    else:
        print("No valid places with priority found in the response.")
else:
    print("No valid filtered places found in the response.")