import requests

class Geocoder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coordinates(self, address):
        params = {
            "address": address,
            "key": self.api_key
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return [location["lat"], location["lng"]]

    def get_three_coordinates(self):
        coordinates = []
        for i in range(3):
            address = input(f"Enter address {i+1}: ")
            coord = self.get_coordinates(address)
            if coord:
                coordinates.append(coord)
        return coordinates