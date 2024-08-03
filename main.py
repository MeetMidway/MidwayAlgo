import numpy as np
import json
from geocoding import Geocoder
from calcGeoMedian import CalculateGeometricMedian
from allplaces import Places
import os
from dotenv import load_dotenv

class Main:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ["GOOGLE_API_KEY"]
        self.geocoder = Geocoder(self.api_key)
        self.geomedian_calculator = CalculateGeometricMedian()
        self.places = Places(self.api_key)

    def run(self):
        coordinates = self.geocoder.get_three_coordinates()
        points = np.array(coordinates)
        
        median = self.geomedian_calculator.geometric_median(points)
        print(f"\nGeometric Median: [{median[0]:.6f}, {median[1]:.6f}]")

        places_nearby = self.places.get_all_places_nearby(median)
        places_info = [{
            "name": place.get("name"), 
            "address": place.get("vicinity"),
            "types": place.get("types")
        }for place in places_nearby]
        
        with open('places_nearby.json', 'w') as f:
            json.dump(places_info, f, indent=4)

if __name__ == "__main__":
    main = Main()
    main.run()
