import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import json
import math
import indices
from pathlib import Path


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
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

# Point class with x, y coordinates and spread (s)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = None  # Spread value will be computed later

    def compute_s(self, all_points, half_value=0.5):
        # Compute s as the distance to the nearest neighbor (or some other criterion)
        min_distance = float('inf')
        for point in all_points:
            if point != self:
                dist = euclidean_distance(self, point)
                if dist < min_distance:
                    min_distance = dist
        # Set s based on the nearest neighbor distance
        self.s = max(half_value* min_distance, 1e-6)  # Avoid s=0

# Cluster class for handling groups of points
class Cluster:
    def __init__(self, point):
        self.points = [point]
        self.centroid = np.array([point.x, point.y])

    def add_point(self, point):
        self.points.append(point)
        # Recalculate the centroid after adding a point
        self.centroid = np.mean([[p.x, p.y] for p in self.points], axis=0)

    def merge(self, cluster):
        for point in cluster.points:
            self.add_point(point)

    def nearest_distance(self, other_cluster):
        min_distance = float('inf')
        closest_pair = None
        for point1 in self.points:
            for point2 in other_cluster.points:
                dist = euclidean_distance(point1, point2)
                if dist < min_distance:
                    min_distance = dist
                    closest_pair = (point1, point2)
        return min_distance, closest_pair

# Calculate intersection points for the normal distributions
def calculate_intersection(mean1, s1, mean2, s2):
    A = 1/s1**2 - 1/s2**2
    B = -2 * (mean1/s1**2 - mean2/s2**2)
    C = (mean1**2/s1**2 - mean2**2/s2**2 + np.log(s2/s1))

    disc = B**2 - 4*A*C
    if disc <= 0 or A == 0:  # Handle zero discriminant or A = 0
        x1 = (-C) / B
        x2 = (-C) / B
    else:
        x1 = (-B + math.sqrt(disc)) / (2 * A)
        x2 = (-B - math.sqrt(disc)) / (2 * A)
    
    return x1, x2

# Determine if two clusters should merge based on overlap
def should_merge(cluster1, cluster2, threshold):
    # Find the nearest points between the two clusters
    _, (nearest_point1, nearest_point2) = cluster1.nearest_distance(cluster2)

    # Get the spread values (s) of the nearest points
    s1 = nearest_point1.s
    s2 = nearest_point2.s

    # Calculate the intersection points between the normal distributions of these two points
    intersection_x = calculate_intersection(nearest_point1.x, s1, nearest_point2.x, s2)
    intersection_y = calculate_intersection(nearest_point1.y, s1, nearest_point2.y, s2)

    # Compute the probability densities at the intersection points for x and y
    height_x = norm.pdf(intersection_x[0], loc=nearest_point1.x, scale=s1)
    height_y = norm.pdf(intersection_y[0], loc=nearest_point1.y, scale=s1)

    # Check if the densities at the intersection points are above the threshold
    return height_x > threshold or height_y > threshold




# Clustering model
def model(points, threshold):
    # Create initial clusters, one for each point
    clusters = [Cluster(point) for point in points]
    half_value = 0.5

    # Compute `s` for each point
    for cluster in clusters:
        for point in cluster.points:
            point.compute_s(points, half_value)

    # Function to merge two clusters
    def merge_clusters(c1, c2):
        c1.merge(c2)
        clusters.remove(c2)

    merge_iterations = 0  # Counter for merge iterations

    # Iterate and merge clusters based on proximity and threshold
    while True:
        merged = False

        # Try to merge clusters based on proximity and threshold
        for i, cluster1 in enumerate(clusters):
            for j, cluster2 in enumerate(clusters):
                if i != j and should_merge(cluster1, cluster2, threshold):
                    merge_clusters(cluster1, cluster2)
                    merged = True
                    merge_iterations += 1
                    break
            if merged:
                break  # Restart merging after a merge

        if not merged:
            break  # No merges happened, stop the loop

    print(f"Number of merge iterations: {merge_iterations}") 
    return [[(p.x, p.y) for p in cluster.points] for cluster in clusters]



# CODE model's cluster function
def code_cluster_function(points):
    threshold = 0.0112  # Define your threshold here
    return model(points, threshold)


# # Implement get_clustering function
# def get_clustering(points, human_clustering, n_trials=1):
#     human_clustering_matrix = indices.to_cluster_matrix(human_clustering)
#     #print this to look at format
#     fms = []
#     clusterings = []

#     for _ in range(n_trials):
#         shuffled_points = points.copy()
#         np.random.shuffle(shuffled_points)
#         clustering = code_cluster_function(shuffled_points)
#         clusterings.append(clustering)
#         fm = indices.fowlkes_mallows(human_clustering_matrix, indices.to_cluster_matrix(clustering))
#         fms.append(fm)

#     # Select the median clustering based on FM index
#     sort_indices = np.argsort(fms)
#     fms = np.array(fms)[sort_indices]
#     clusterings = [clusterings[i] for i in sort_indices]
#     median_index = len(fms) // 2
#     return fms[median_index], clusterings[median_index]

def get_clustering(trials, target_uuid):
    """
    Computes clustering for the trial matching the specified UUID and compares it to human clustering
    using the Fowlkes-Mallows index.

    Parameters:
        trials (list): List of trials containing clusters and points data.
        target_uuid (str): The UUID to identify the specific trial.

    Returns:
        tuple: Fowlkes-Mallows index and the resulting clustering from the model.
    """
    # Find the trial with the matching UUID
    trial = next((t for t in trials if t.get("unique_uuid") == target_uuid), None)
    if not trial:
        raise ValueError(f"No trial found with UUID {target_uuid}")

    # Extract human clustering from trial
    human_clustering = [
        [[point["x"], point["y"]] for point in cluster["points"]]
        for cluster in trial["clusters"]
    ]

    # Remove empty clusters (if any)
    human_clustering = [cluster for cluster in human_clustering if len(cluster) > 0]

    # Convert human clustering to pairwise cluster matrix
    human_clustering_matrix = indices.to_cluster_matrix(human_clustering)

    # Concatenate all points from human clustering
    points = np.concatenate(human_clustering)

    # Create Point objects for the clustering algorithm
    point_objects = [Point(x, y) for x, y in points]

    # Run the clustering model to get predicted clusters
    predicted_clusters = code_cluster_function(point_objects)

    # Convert predicted clusters to pairwise cluster matrix
    predicted_clusters = [
        np.array(cluster) for cluster in predicted_clusters if len(cluster) > 0
    ]
    predicted_clustering_matrix = indices.to_cluster_matrix(predicted_clusters)

    # Compute the Fowlkes-Mallows index
    fm_index = indices.fowlkes_mallows(human_clustering_matrix, predicted_clustering_matrix)

    return fm_index, predicted_clusters



######Need to eidt
#how u import a trial: load_file("normalized_clustering_trials/6.json")



# Graphing the final clusters
def plot_clusters(clusters):
    color_list = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'pink', 'brown', 'black']
    for i, cluster in enumerate(clusters):
        cluster_points = np.array([[point.x, point.y] for point in cluster.points])
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color_list[i % len(color_list)], label=f'Cluster {i+1}')

    plt.title("Final Clusters")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

def plot_numpy_clusters(clusters):
    """
    Plots the clusters on a scatter plot.

    Parameters:
        clusters (list): List of clusters, where each cluster is a numpy array of points.
    """
    color_list = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'pink', 'brown', 'black']
    
    # Iterate over each cluster and plot its points
    for i, cluster in enumerate(clusters):
        cluster_points = np.array(cluster)  # Ensure each cluster is a numpy array
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                    color=color_list[i % len(color_list)], label=f'Cluster {i+1}')
    
    plt.title("Final Clusters")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()



def load_file(filename):
    with Path(filename).open() as f:
        return json.load(f)

# Example usage
if __name__ == "__main__":
    # Load JSON stimulus (adjust path as needed)
    with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\9d1031bf-0931-4a8c-9aae-9767a622bcdb.json") as f:
    #with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\avni-sample.json") as f:
        stimulus = json.load(f)
        points = [Point(point["x"], point["y"]) for point in stimulus["points"]]
        human_clustering =  load_file("clustering-experiment-public-release\\clustering-analysis\\data\\normalized_clustering_trials\\6.json")

        # UUID to look for
        target_uuid = "9d1031bf-0931-4a8c-9aae-9767a622bcdb"

    try:
        # Compute the clustering and FM index for the trial with the target UUID
        fm, clustering = get_clustering(human_clustering, target_uuid)
        print(f"Fowlkes-Mallows Index: {fm}")
        print(f"Clusters: {clustering}")

        # Plot the resulting clusters
        plot_numpy_clusters(clustering)
    except ValueError as e:
        print(e)

        fm, clustering = get_clustering(points, human_clustering)
        print(f"Fowlkes-Mallows Index: {fm}")
        print(f"Clusters: {clustering}")


    threshold = 0.0112  # Set a threshold for merging
    clusters = model(points, threshold)
    
    
    # Print the number of clusters
    print(f"Number of clusters: {len(clusters)}")

    # Plot the resulting clusters
    plot_numpy_clusters(clusters)
