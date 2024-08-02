import numpy as np

class CalculateGeometricMedian:
    def geometric_median(self, X, eps=1e-5):
        """
        Compute the geometric median of a set of points using the Weiszfeld algorithm.
        
        Parameters:
        X : array-like, shape (n_points, n_dimensions)
            The input points.
        eps : float, optional
            The convergence threshold.
            
        Returns:
        median : array, shape (n_dimensions,)
            The geometric median.
        """
        y = np.mean(X, axis=0)
        print(f"Initial guess (mean): {y}")

        while True:
            D = np.sqrt(((X - y) ** 2).sum(axis=1))
            nonzeros = (D != 0)

            Dinv = 1 / D[nonzeros]
            W = Dinv / Dinv.sum()
            T = (X[nonzeros] * W[:, None]).sum(axis=0)

            num_zeros = len(X) - np.sum(nonzeros)
            if num_zeros == 0:
                y1 = T
            elif num_zeros == len(X):
                return y
            else:
                R = (X[~nonzeros]).mean(axis=0)
                y1 = (num_zeros * R + T) / len(X)

            change = np.linalg.norm(y - y1)
            print(f"Updated guess: {y1}, Change: {change}")

            if change < eps:
                return y1

            y = y1


if __name__ == "__main__":
    # Example points, replace with friends
    points = np.array([
        [1, 2],
        [3, 4],
        [5, 5],
        [7, 8]
    ])

    calcGeoMedian = CalculateGeometricMedian()

    median = calcGeoMedian.geometric_median(points)
    print("Geometric Median:", median)

    # Printing with decimal points
    print(f"Geometric Median: ({median[0]:.6f}, {median[1]:.6f})")