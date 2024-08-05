import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import json

class Places:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
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


# # Example usage
# if __name__ == "__main__":
#     api_key = "YOUR_GOOGLE_API_KEY"
#     location = (40.712776, -74.005974) 
#     places = Places(api_key)
#     all_places = places.get_all_places_nearby(location)
#     print(f"Total places found: {len(all_places)}")

#     with open('all_places.json', 'w') as f:
#         json.dump(all_places, f, indent=4)
