import numpy as np
from geocoding import Geocoder
from calcGeoMedian import CalculateGeometricMedian

class Main:
    def __init__(self):
        self.api_key = "AIzaSyBpNxil9cypEP75XM9G1L12XkepUbqSwtI"
        self.geocoder = Geocoder(self.api_key)
        self.geomedian_calculator = CalculateGeometricMedian()

    def run(self):
        coordinates = self.geocoder.get_three_coordinates()
        points = np.array(coordinates)

        median = self.geomedian_calculator.geometric_median(points)

        for i, coord in enumerate(coordinates):
            print(f"Address {i+1}: [{coord[0]:.6f}, {coord[1]:.6f}]")

        print(f"\nGeometric Median: [{median[0]:.6f}, {median[1]:.6f}]")

if __name__ == "__main__":
    main = Main()
    main.run()