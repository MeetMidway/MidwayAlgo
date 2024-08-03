# Imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


def text_search(params, headers):
    # print(params)
    text_search_url = "https://places.googleapis.com/v1/places:searchText"
    response = requests.post(url=text_search_url, json=params, headers=headers).json()

    return response 

if __name__ == '__main__':
    params = {
        "textQuery": "Pizza places",
        "pageSize": 2,
        "locationRestriction": {
            "rectangle": {
                "low": {
                "latitude": 40.477398,
                "longitude": -74.259087
                },
                "high": {
                "latitude": 40.91618,
                "longitude": -73.70018
                }
            }
        }
    }

    headers = {
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress',
        'X-Goog-Api-Key': GOOGLE_API_KEY
    }
    print(text_search(params, headers))
