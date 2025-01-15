# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm
# import json
# import math
# import itertools

# def model(points, s, t):
#     clusters = [Cluster(s, p) for p in points]

#     # Calculate `s` for each cluster based on the initial points
#     for cluster in clusters:
#         cluster.compute_s(points)

#     # Helper function used within the merging loop to call merge() and remove the merged cluster from the list
#     def merge_clusters(c1, c2):
#         c1.merge(c2)
#         print("Cluster merged.")
#         clusters.remove(c2)
#         return True

#     while True:
#         merged = False

#         for i, cluster1 in enumerate(clusters):  # Iterating from first cluster
#             for j, cluster2 in enumerate(clusters):  # Iterating from second cluster 
#                 if i != j and should_merge(cluster1, cluster2, t, s):
#                     print("i =", i)
#                     print("j =", j)
#                     merged = merge_clusters(cluster1, cluster2)
#                     break 
#             if merged:
#                 break  # Break outer loop and restart after a merge

#         if not merged:
#             break  # No merges occurred; exit the loop

#     return clusters

# # Class to define the properties of a cluster

# class Cluster:
#     def __init__(self, s, p):
#         self.points = [p]
#         self.centroid = 0
#         self.s = s

#     def compute_s(self, all_points):
#         if len(self.points) == 1:
#             # If cluster has only one point, find the nearest point in the entire dataset
#             single_point = self.points[0]
#             min_distance = float('inf')
            
#             for point in all_points:
#                 if point != single_point:
#                     dist = euclidean_distance(single_point, point)
#                     if dist < min_distance:
#                         min_distance = dist
            
#             # Set s based on the nearest neighbor distance
#             # This is because the distance to the other points is trivialized
#             self.s = 0.5 * min_distance
#         else:
#             # For clusters with more than one point, use the standard deviation
#             self.s = np.std(self.points, axis=0)[0]  # Use the standard deviation along one dimension

#     def merge(self, cluster):
#         self.points += cluster.points  # Add all points from the merging cluster
#         _, (nearest_point_self, nearest_point_other) = self.nearest_distance(cluster)
#         self.s = 0.5 * self.s * euclidean_distance(nearest_point_self, nearest_point_other)
#         self.centroid = np.mean(self.points, axis=0)

#     def __repr__(self):  # Return string representation of cluster
#         return str(len(self.points))

#     def nearest_distance(self, other_cluster):
#         min_distance = float('inf')
#         closest_pair = None
#         for point1 in self.points:
#             for point2 in other_cluster.points:
#                 dist = euclidean_distance(point1, point2)
#                 if dist < min_distance:
#                     min_distance = dist
#                     closest_pair = (point1, point2)
#         return min_distance, closest_pair

# def euclidean_distance(p1, p2):
#     return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# def calculate_intersection(mean1, s1, mean2, s2):
#     print("S1 =", s1)
#     print("S2 =", s2)
#     A = 1/s1**2 - 1/s2**2
#     print("A =", A)
#     B = -2 * (mean1/s1**2 - mean2/s2**2)
#     print("B =", B)
#     C = (mean1**2/s1**2 - mean2**2/s2**2 + np.log(s2/s1))
#     print("C =", C)

#     disc = B**2 - 4*A*C
    
#     if disc <= 0 or A == 0:  # Handle zero discriminant or A = 0
#         x1 = (-C) / B
#         x2 = (-C) / B
#     else:
#         x1 = (-B + math.sqrt(disc)) / (2 * A)
#         x2 = (-B - math.sqrt(disc)) / (2 * A)
#     print("x1 =", x1)
#     print("x2 =", x2)
#     return x1, x2

# # Determine if two clusters should merge based on overlap
# def should_merge(cluster1, cluster2, threshold, global_s):
#     # Find nearest points between clusters
#     _, (nearest_point1, nearest_point2) = cluster1.nearest_distance(cluster2)

#     # setting s1 based on the cluster's inner values
#     s1 = cluster1.s
#     s2 = cluster2.s

#     intersection_x = calculate_intersection(nearest_point1[0], s1, nearest_point2[0], s2)
#     intersection_y = calculate_intersection(nearest_point1[1], s2, nearest_point2[1], s2)

#     height_x = norm.pdf(intersection_x[0], loc=nearest_point1[0], scale=s1)
#     print("height_x =", height_x)
#     height_y = norm.pdf(intersection_y[0], loc=nearest_point1[1], scale=s1)
#     print("height_y =", height_y)
#     return height_x > threshold or height_y > threshold


# # Graphing

# with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\0a0009dc-2b19-4a23-aa5b-b73250d4a506.json") as f:
# #with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\avni-sample.json") as f:
#     stimulus = json.load(f)
#     points = [[point["x"], point["y"]] for point in stimulus["points"]]
#     points = np.array(points)
#     print(points)
#     clusters = model(points, 100, 0.01)
#     print(clusters)
#     print("Number of clusters:", len(clusters))
#     print("Clusters:", clusters)


# color_list = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'pink', 'brown', 
#               'black']  
# for i, cluster in enumerate(clusters):
#     cluster_points = np.array(cluster.points)
#     plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color_list[i % len(color_list)], label=f'Cluster {i+1}')

# plt.title("Final Clusters")
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.legend()
# plt.show()



# later
# thresh_range = 2 * np.logspace(-4, -1, num=25, endpoint=True, base=10.0, dtype=None, axis=0) 
# for thresh in thresh_range:
#     clusters = model(points, 100, thresh)
#     print("thresh =", thresh)
#     print("Number of clusters:", len(clusters))
#     print("Clusters:", clusters)
#     print("=======")
    


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import json
import math

def model(points, initial_s, threshold):
    # Initialize clusters, each with a single point
    clusters = [Cluster(initial_s, p) for p in points]

    # Calculate `s` for each cluster based on the initial points
    for cluster in clusters:
        cluster.compute_s(points)

    # Helper function to merge clusters and remove the merged one from the list
    def merge_clusters(c1, c2):
        c1.merge(c2)
        print("Cluster merged.")
        clusters.remove(c2)
        return True

    # Main loop to merge clusters until no more merges are possible
    while True:
        merged = False
        for i, cluster1 in enumerate(clusters):
            for j, cluster2 in enumerate(clusters):
                if i != j and should_merge(cluster1, cluster2, threshold):
                    print("Merging clusters at indices:", i, j)
                    merged = merge_clusters(cluster1, cluster2)
                    break
            if merged:
                break  # Restart merging from the beginning after a merge

        if not merged:
            break  # Exit if no merges occurred in a pass

    return clusters

class Cluster:
    def __init__(self, initial_s, point):
        self.points = [point]  # Initialize with one point
        self.s = initial_s  # Dispersion parameter
        self.centroid = np.array(point)  # Initialize centroid

    def compute_s(self, all_points):
        if len(self.points) == 1:
            # Find nearest point in the dataset for clusters of size 1
            single_point = self.points[0]
            min_distance = float('inf')
            for point in all_points:
                if not np.array_equal(point, single_point):
                    dist = euclidean_distance(single_point, point)
                    if dist < min_distance:
                        min_distance = dist
            # Set s as half of the distance to the nearest neighbor
            self.s = 0.5 * min_distance
        else:
            # Use standard deviation as s for larger clusters
            self.s = np.std(self.points, axis=0).mean()  # Mean of std deviations along x and y

    def merge(self, other):
        # Combine points and recalculate centroid and s
        self.points.extend(other.points)
        _, (nearest_point_self, nearest_point_other) = self.nearest_distance(other)
        self.s = 0.5 * euclidean_distance(nearest_point_self, nearest_point_other)
        self.centroid = np.mean(self.points, axis=0)

    def nearest_distance(self, other_cluster):
        # Find the closest pair of points between this cluster and another
        min_distance = float('inf')
        closest_pair = None
        for point1 in self.points:
            for point2 in other_cluster.points:
                dist = euclidean_distance(point1, point2)
                if dist < min_distance:
                    min_distance = dist
                    closest_pair = (point1, point2)
        return min_distance, closest_pair

    def __repr__(self):
        return f"Cluster of size {len(self.points)} at {self.centroid}"

def euclidean_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def calculate_intersection(mean1, s1, mean2, s2):
    # Calculate intersection points between two normal distributions
    A = 1/s1**2 - 1/s2**2
    B = -2 * (mean1/s1**2 - mean2/s2**2)
    C = (mean1**2/s1**2 - mean2**2/s2**2 + np.log(s2/s1))

    disc = B**2 - 4*A*C
    if disc <= 0 or A == 0:
        return None  # No intersection or parallel lines
    x1 = (-B + math.sqrt(disc)) / (2 * A)
    x2 = (-B - math.sqrt(disc)) / (2 * A)
    return x1, x2

def should_merge(cluster1, cluster2, threshold):
    # Determine if two clusters should merge by checking overlap in both x and y axes
    _, (nearest_point1, nearest_point2) = cluster1.nearest_distance(cluster2)
    s1, s2 = cluster1.s, cluster2.s
    intersection_x = calculate_intersection(nearest_point1[0], s1, nearest_point2[0], s2)
    intersection_y = calculate_intersection(nearest_point1[1], s1, nearest_point2[1], s2)

    if intersection_x and intersection_y:
        # Calculate the height of overlap in normal distributions along x and y
        height_x = norm.pdf(intersection_x[0], loc=nearest_point1[0], scale=s1)
        height_y = norm.pdf(intersection_y[0], loc=nearest_point1[1], scale=s1)
        return height_x > threshold or height_y > threshold
    return False

# Plotting the final clusters
def plot_clusters(clusters):
    color_list = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'pink', 'brown', 'black']
    for i, cluster in enumerate(clusters):
        cluster_points = np.array(cluster.points)
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color_list[i % len(color_list)], label=f'Cluster {i+1}')
    plt.title("Final Clusters")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# # Load points and create clusters
# with open("clustering-experiment-public-release/clustering-analysis/stimuli/experiment-1-2-3/stimuli_json/0a0009dc-2b19-4a23-aa5b-b73250d4a506.json") as f:
#     stimulus = json.load(f)
#     points = np.array([[point["x"], point["y"]] for point in stimulus["points"]])
#     clusters = model(points, 100, 0.01)
#     print("Final Clusters:", clusters)
#     print("Number of clusters:", len(clusters))




# Parameters for the two normal distributions
mean1, s1 = 0, 1
mean2, s2 = 1, 1

# Calculate intersection points
intersections = calculate_intersection(mean1, s1, mean2, s2)
print("Intersection points:", intersections)

# Create x values for the plot
x = np.linspace(-3, 4, 500)

# Plot the two normal distributions
y1 = norm.pdf(x, mean1, s1)
y2 = norm.pdf(x, mean2, s2)

plt.plot(x, y1, label=f'Normal(μ={mean1}, σ={s1})', color='blue')
plt.plot(x, y2, label=f'Normal(μ={mean2}, σ={s2})', color='green')

# Mark the intersection points if they exist
if intersections:
    for ix in intersections:
        plt.plot(ix, norm.pdf(ix, mean1, s1), 'ro')  # Red dot at each intersection
        plt.axvline(ix, color='red', linestyle='--', alpha=0.5)  # Vertical line for visual clarity

# Add plot details
plt.title("Intersection of Two Normal Distributions")
plt.xlabel("X")
plt.ylabel("Probability Density")
plt.legend()
plt.show()


# Plot clusters
plot_clusters(clusters)
