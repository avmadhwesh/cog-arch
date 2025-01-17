import numpy as np
import matplotlib.pyplot as plt
import math
import json

# Helper function to compute Euclidean distance
def euclidean_distance(p1, p2):
    """
    Computes the Euclidean distance between two points.

    Parameters:
        p1 (Point): The first point with x and y attributes.
        p2 (Point): The second point with x and y attributes.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

# Point class with x, y coordinates and spread (s)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = None  # Spread value will be computed later

    def compute_s(self, all_points):
        """
        Computes the spread (s) for the point based on the nearest neighbor.

        Parameters:
            all_points (list): List of all points.

        Returns:
            None
        """
        min_distance = float('inf')
        for point in all_points:
            if point != self:
                dist = euclidean_distance(self, point)
                if dist < min_distance:
                    min_distance = dist
        # Set s based on the nearest neighbor distance
        self.s = max(0.5 * min_distance, 1e-6)  # Avoid s=0

# 2D Gaussian function to compute influence at a grid point
def gaussian_2d(x, y, center_x, center_y, s):
    """
    Computes the 2D Gaussian value at (x, y) for a given center and spread.

    Parameters:
        x (array): X-coordinate grid.
        y (array): Y-coordinate grid.
        center_x (float): X-coordinate of the Gaussian center.
        center_y (float): Y-coordinate of the Gaussian center.
        s (float): Spread (standard deviation).

    Returns:
        array: Gaussian values at each grid point.
    """
    return np.exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * s ** 2))

# Compute the cumulative influence function f_t(x, y)
def compute_ft(points, grid_x, grid_y):
    """
    Computes the cumulative influence function f_t(x, y) on a grid.

    Parameters:
        points (list): List of Point objects with x, y, and s attributes.
        grid_x, grid_y (array): Meshgrid of x and y coordinates.

    Returns:
        array: Cumulative influence function f_t(x, y) on the grid.
    """
    f_t = np.zeros_like(grid_x)  # Initialize the cumulative function with zeros
    for point in points:
        f_t += gaussian_2d(grid_x, grid_y, point.x, point.y, point.s)
    return f_t

# Determine optimal threshold based on f_t(x, y)
def determine_optimal_threshold(f_t):
    """
    Determines the optimal threshold for clustering based on f_t(x, y).

    Parameters:
        f_t (array): Cumulative influence function values.

    Returns:
        float: Optimal threshold value.
    """
    max_value = np.max(f_t)  # Maximum value of f_t(x, y)
    return 0.5 * max_value  # Set threshold as 50% of the peak value

# Extract clusters based on the threshold
def extract_clusters(points, f_t, grid_x, grid_y, threshold):
    """
    Extract clusters of points based on the threshold.

    Parameters:
        points (list): List of Point objects.
        f_t (array): Cumulative influence function values.
        grid_x, grid_y (array): Meshgrid of x and y coordinates.
        threshold (float): Threshold value for clustering.

    Returns:
        list: List of clusters, where each cluster is a list of points.
    """
    clusters = []
    visited = set()
    merge_count = 0  # Counter for merge iterations

    for i, point in enumerate(points):
        if i in visited:
            continue
        cluster = [point]
        visited.add(i)
        for j, other_point in enumerate(points):
            if j not in visited:
                if f_t[np.argmin(abs(grid_x[0] - other_point.x)), np.argmin(abs(grid_y[:, 0] - other_point.y))] >= threshold:
                    cluster.append(other_point)
                    visited.add(j)
                    merge_count += 1
        clusters.append(cluster)
    print(f"Number of merge iterations: {merge_count}")
    return clusters

# Plot the cumulative influence function and clusters
def plot_clusters(grid_x, grid_y, f_t, points, threshold):
    """
    Plots the cumulative influence function and highlights clusters based on a threshold.

    Parameters:
        grid_x, grid_y (array): Meshgrid of x and y coordinates.
        f_t (array): Cumulative influence function values.
        points (list): List of Point objects.
        threshold (float): Threshold value for clustering.

    Returns:
        None
    """
    # Plot the influence function
    plt.contourf(grid_x, grid_y, f_t, levels=50, cmap='viridis')
    plt.colorbar(label="f_t(x, y)")
    plt.title("Cumulative Influence Function f_t(x, y)")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Highlight clusters by thresholding
    plt.contour(grid_x, grid_y, f_t, levels=[threshold], colors='red', linewidths=1.5, label="Cluster Contour")

    # Overlay original points
    for point in points:
        plt.scatter(point.x, point.y, color='white', edgecolor='black')

    plt.show()

# Main function to execute the clustering process
def main():
    # Example set of points
    # points = [
    #     Point(2, 3), Point(3, 3), Point(5, 6), Point(8, 8),
    #     Point(1, 8), Point(9, 1), Point(4, 5), Point(6, 7)
    # ]
    # with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\0a0009dc-2b19-4a23-aa5b-b73250d4a506.json") as f:
    with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\9d1031bf-0931-4a8c-9aae-9767a622bcdb.json") as f:

    # with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\avni-sample.json") as f:
        stimulus = json.load(f)
        points = [Point(point["x"], point["y"]) for point in stimulus["points"]]

    # Compute s for each point based on the nearest neighbor
    for point in points:
        point.compute_s(points)

    # Define the grid where f_t(x, y) will be evaluated
    x_min, x_max = 0, 10
    y_min, y_max = 0, 10
    resolution = 100

    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    grid_x, grid_y = np.meshgrid(x, y)

    # Compute the cumulative influence function f_t(x, y)
    f_t = compute_ft(points, grid_x, grid_y)

    # Determine the optimal threshold
    threshold = determine_optimal_threshold(f_t)
    # threshold = 0.1110709
    print(f"Optimal Threshold: {threshold}")

    # Extract clusters
    clusters = extract_clusters(points, f_t, grid_x, grid_y, threshold)

    # Plot the results
    plot_clusters(grid_x, grid_y, f_t, points, threshold)

    # Print the clusters
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i + 1}:")
        for point in cluster:
            print(f"    ({point.x}, {point.y})")

if __name__ == "__main__":
    main()
