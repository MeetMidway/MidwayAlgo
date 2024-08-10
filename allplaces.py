import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import json

class Places:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        self.photo_url = "https://maps.googleapis.com/maps/api/place/photo"
        self.keywords = ["shop", "store", "services", "center", "place", "point", "location", "food", "drink", "entertainment", "leisure", "landmark", "parks", "playgrounds"]

    def get_all_places_nearby(self, location, radius=3000):
        all_places = []
        seen_place_ids = set()
        threads = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for keyword in self.keywords:
                print(f"Fetching places with keyword: {keyword}")
                threads.append(executor.submit(self._fetch_places, location, radius, keyword, all_places, seen_place_ids))

            for task in threads:
                try:
                    task.result()  # Ensure all threads complete
                except Exception as e:
                    print(f"Error occurred in thread: {e}")

        return all_places

    def _fetch_places(self, location, radius, keyword, all_places, seen_place_ids):
        params = {
            "location": f"{location[0]},{location[1]}",
            "radius": radius,
            "keyword": keyword,
            "key": self.api_key
        }

        while True:
            response = self._make_request(self.base_url, params)
            if not response:
                break
            data = response.json()

            if data["status"] == "OK":
                for place in data["results"]:
                    if place["place_id"] not in seen_place_ids:
                        place_details = self.get_place_details(place["place_id"])
                        place["rating"] = place_details.get("rating")
                        place["user_ratings_total"] = place_details.get("user_ratings_total")
                        place["photo_url"] = self.get_place_photo_url(place_details)
                        all_places.append(place)
                        seen_place_ids.add(place["place_id"])

                if "next_page_token" in data:
                    params["pagetoken"] = data["next_page_token"]
                    time.sleep(2)  
                    break
            else:
                print(f"Error fetching places with keyword {keyword}: {data['status']}")
                break

    def get_place_details(self, place_id):
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "key": self.api_key
        }

        response = self._make_request(details_url, params)
        if not response:
            return {}
        return response.json().get("result", {})

    def get_place_photo_url(self, place_details):
        photos = place_details.get("photos")
        if not photos:
            return None

        photo_reference = photos[0].get("photo_reference")
        if not photo_reference:
            return None

        photo_params = {
            "maxwidth": 400,  # You can change this value depending on the desired image size
            "photoreference": photo_reference,
            "key": self.api_key
        }

        return f"{self.photo_url}?maxwidth={photo_params['maxwidth']}&photoreference={photo_params['photoreference']}&key={self.api_key}"

    def _make_request(self, url, params, retries=3):
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    return response
            except requests.RequestException as e:
                print(f"Request error: {e}")
            time.sleep(2)
        return None
