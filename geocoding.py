import requests

def get_coordinates(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return [location["lat"], location["lng"]]




api_key = "AIzaSyBpNxil9cypEP75XM9G1L12XkepUbqSwtI"
address = input("Enter an address: ")
coordinates = get_coordinates(address, api_key)
print(coordinates)