import requests
from html import unescape
from bs4 import BeautifulSoup
from geopy.distance import geodesic

def get_coordinates(api_key, address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(base_url, params={"address": address, "key": api_key})
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise ValueError(f"Geocoding API error: No results found for address '{address}'")

def get_distance(coord1, coord2):
    return geodesic(coord1, coord2).miles

def get_directions(api_key, origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    return response.json()['routes'][0]['legs'][0]['steps']

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return unescape(soup.get_text())

# Example usage
midpoint_address = "1 Infinite Loop, Cupertino, CA"  # Random midpoint address
addresses = [
    "1600 Amphitheatre Parkway, Mountain View, CA",
    "500 Terry Francois Blvd, San Francisco, CA",
    "1355 Market St, San Francisco, CA"
]

api_key = "AIzaSyBpNxil9cypEP75XM9G1L12XkepUbqSwtI"

# Get coordinates for midpoint and addresses
midpoint_coord = get_coordinates(api_key, midpoint_address)
coordinates = {address: get_coordinates(api_key, address) for address in addresses}

# Calculate distances from midpoint to each address
distances = {address: get_distance(midpoint_coord, coord) for address, coord in coordinates.items()}

# Sort addresses by distance from midpoint
sorted_addresses = sorted(distances, key=distances.get)

# Generate directions from midpoint to each address
directions = []
for address in sorted_addresses:
    destination = coordinates[address]
    steps = get_directions(api_key, midpoint_coord, destination)
    directions.append({
        "destination": address,
        "steps": steps
    })
    # Update the midpoint to the current destination for the next segment
    midpoint_coord = destination

# Print directions
print(f"Starting from the midpoint: {midpoint_address}\n")
for direction in directions:
    print(f"Directions to {direction['destination']}:")
    for step in direction['steps']:
        plain_text_instruction = clean_html(step['html_instructions'])
        print(plain_text_instruction)
    print(f"Welcome to {direction['destination']}! Enjoy your time.\n")

