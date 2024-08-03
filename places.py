# Imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


def text_search(params):
    print(params)
    text_search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    response = requests.get(text_search_url, params).json()

    return response 

if __name__ == '__main__':
    params = {
        "query": "Pizza places",
        "key": GOOGLE_API_KEY,
        "pageSize": 2,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": 38.897957,
                    "longitude": -77.036560
                },
                "radius": 2000.0 # Distance in meters
            }
        }
    }
    print(text_search(params))
