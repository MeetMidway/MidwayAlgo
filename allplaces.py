import requests

class Places:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    def get_all_places_nearby(self, location, radius=1000):
        params = {
            "location": f"{location[0]},{location[1]}",
            "radius": radius,
            "key": self.api_key
        }

        places = []
        while True:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if data["status"] == "OK":
                places.extend(data["results"])
                if "next_page_token" in data:
                    params["pagetoken"] = data["next_page_token"]

                    import time
                    time.sleep(2) #this is because google requires a short time delay in  token use since we're generating a massive json file
                else:
                    break
            else:
                break

        return places
