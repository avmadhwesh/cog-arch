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


# Implement get_clustering function
def get_clustering(points, human_clustering, n_trials=1):
    human_clustering_matrix = indices.to_cluster_matrix(human_clustering)
    #print this to look at format
    fms = []
    clusterings = []

    for _ in range(n_trials):
        shuffled_points = points.copy()
        np.random.shuffle(shuffled_points)
        clustering = code_cluster_function(shuffled_points)
        clusterings.append(clustering)
        fm = indices.fowlkes_mallows(human_clustering_matrix, indices.to_cluster_matrix(clustering))
        fms.append(fm)

    # Select the median clustering based on FM index
    sort_indices = np.argsort(fms)
    fms = np.array(fms)[sort_indices]
    clusterings = [clusterings[i] for i in sort_indices]
    median_index = len(fms) // 2
    return fms[median_index], clusterings[median_index]



###COPIED

def cluster_and_compare_trial(trial, anderson_c, n_trials):

    human_clustering = []
    for cluster_data in trial['clusters']:
        np.array(human_clustering.append([[a["x"], a["y"]] for a in cluster_data['points']]))

    human_clustering_matrix = indices.to_cluster_matrix(human_clustering)
    points = np.concatenate(human_clustering)

    pid = str(trial['participant_id'])

    params = {"human_clustering": human_clustering, "c": anderson_c,
              "sustain_global_params": np.array([23.06774144, 27.03527136,  0.88381838,  0.07051525]),
              "sustain_per_participant_params": SUSTAIN_PER_PARTICIPANT_PARAMS[pid],
              "kmeans_per_trial_params": len(human_clustering),
              "kmeans_per_participant_params": min(len(human_clustering), KMEANS_PER_PARTICIPANT_PARAMS[pid]),
              "kmeans_global_params": min(len(human_clustering), KMEANS_GLOBAL_N_CLUSTERS)
              }

    results = []

    for algo in ALGORITHMS:
        fm, clustering = get_many_clusterings(human_clustering_matrix,
                             points, lambda points: algo["func"](points, params),
                             n_trials)

        _, indexes = indices.to_standard_form(clustering)

        results.append(ComparisonResult(algo["name"], fm, clustering, indexes))

    return results

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


def load_file(filename):
    with Path(filename).open() as f:
        return json.load(f)

# Example usage
if __name__ == "__main__":
    # Load JSON stimulus (adjust path as needed)
    with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\0a0009dc-2b19-4a23-aa5b-b73250d4a506.json") as f:
    #with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\avni-sample.json") as f:
        stimulus = json.load(f)
        points = [Point(point["x"], point["y"]) for point in stimulus["points"]]
        human_clustering =  load_file("clustering-experiment-public-release\\clustering-analysis\\data\\normalized_clustering_trials\\6.json")


        fm, clustering = get_clustering(points, human_clustering)
        print(f"Fowlkes-Mallows Index: {fm}")
        print(f"Clusters: {clustering}")
        
    # Run the clustering algorithm

    #many thresholds
    # thresh_range = 2 * np.logspace(-4, -1, num=25, endpoint=True, base=10.0)

    # for thresh in thresh_range:
    #     clusters = model(points, thresh)
    #     # Print the current threshold value (with 4 decimal places for clarity)
    #     print(f"Threshold = {thresh:.4f}")
    #     # Print the number of clusters found
    #     print(f"Number of clusters: {len(clusters)}")
    #     # Print details about each cluster
    #     for i, cluster in enumerate(clusters):
    #         print(f"Cluster {i+1} (Size: {len(cluster.points)}):")
    #         # # Optionally, print the centroid and the points in the cluster (depending on how much info you want)
    #         # print(f"  Centroid: {cluster.centroid}")
    #         # print(f"Cluster {cluster.id} (Size: {len(cluster.points)}):")
    #         # print(f"  Centroid: {cluster.centroid}")
    #         # print("  Points:", [(point.x, point.y) for point in cluster.points])
    #         print("Num of Points:", len(cluster.points))
    #     print("=======")


    threshold = 0.0112  # Set a threshold for merging
    clusters = model(points, threshold)
    
    
    # Print the number of clusters
    print(f"Number of clusters: {len(clusters)}")

    # Plot the resulting clusters
    plot_clusters(clusters)
