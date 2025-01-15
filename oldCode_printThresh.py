import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import json
import math
import itertools

def model(points, s, t):
    clusters = [Cluster(s, p) for p in points]

    def merge_clusters(c1, c2):
        c1.merge(c2)
        print("Cluster merged.")
        clusters.remove(c2)
        return True

    # Main merging loop
    while True:
        merged = False

        for i, cluster1 in enumerate(clusters): #outer
            for j, cluster2 in enumerate(clusters): #inner
                if i != j and should_merge(cluster1, cluster2, t, s):
                    # print("i = ", i)
                    # print("j = ", j)
                    merged = merge_clusters(cluster1, cluster2)
                    break 
            if merged:
                break  # Break outer loop and restart after a merge

        if not merged:
            break  # No merges occurred; exit the loop

    return clusters


class Cluster:
    def __init__(self, s, p):
        self.points = [p]
        self.centroid = 0
        self.s = s

    def merge(self, cluster):
        self.points += cluster.points
        # update s
        # self.s = 1/2 * s * euclidean_distance(self.centroid, cluster.centroid)
        # CHANGE - need to compare the two nearest points in a cluster and then do merge caclulations based on those, not centroid
        # update the centroid
        _, (nearest_point_self, nearest_point_other) = self.nearest_distance(cluster)
        self.s = 0.5 * self.s * euclidean_distance(nearest_point_self, nearest_point_other)
        self.centroid = np.mean(self.points, axis=0)

    def __repr__(self): #return string representation of cluster
        return str(len(self.points))

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

def euclidean_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def calculate_intersection(mean1, s1, mean2, s2):
    # print("S1 = ", s1)
    # print("S2 = ", s2)
    A = 1/s1**2 - 1/s2**2
    # print("A = ", A)
    B = -2 * (mean1/s1**2 - mean2/s2**2)
    # print("B = ", B)
    C = (mean1**2/s1**2 - mean2**2/s2**2 + np.log(s2/s1))
    # print("C = ", C)

    disc = B**2 - 4*A*C
    
    if disc <= 0 or A == 0:  # Handle zero discriminant or A = 0
        x1 = (-C) / B
        x2 = (-C) / B
        # return None
    else:
        x1 = (-B + math.sqrt(disc)) / (2 * A)
        x2 = (-B - math.sqrt(disc)) / (2 * A)
    # print("x1 = ", x1)
    # print("x2 = ", x2)
    return x1, x2

# overlap
def should_merge(cluster1, cluster2, threshold, global_s):

        # Find nearest points between clusters
    _, (nearest_point1, nearest_point2) = cluster1.nearest_distance(cluster2)
    #fix - comment n use vars
    
    #no global s- for size == 1, just use the s based on dist to nearest neighbor
    s1 = global_s if len(cluster1.points) == 1 else np.std(cluster1.points, axis=0)[0] #fix
    s2 = global_s if len(cluster2.points) == 1 else np.std(cluster2.points, axis=0)[0]

    intersection_x = calculate_intersection(nearest_point1[0], s1, nearest_point2[0], s2)
    intersection_y = calculate_intersection(nearest_point1[1], s2, nearest_point2[1], s2)

    height_x = norm.pdf(intersection_x[0], loc=nearest_point1[0], scale=s1)
    # print("height_x =", height_x)
    height_y = norm.pdf(intersection_y[0], loc=nearest_point1[1], scale=s1)
    # print("height_y =", height_y)
    return height_x > threshold or height_y > threshold



# Graphing

with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\0a0009dc-2b19-4a23-aa5b-b73250d4a506.json") as f:
#with open("clustering-experiment-public-release\\clustering-analysis\\stimuli\\experiment-1-2-3\\stimuli_json\\avni-sample.json") as f:
    stimulus = json.load(f)
    points = [[point["x"], point["y"]] for point in stimulus["points"]]
    #make more obviously clustered stimuli
    points = np.array(points)
    # print(points)
    thresh_range = 2 * np.logspace(-4, -1, num=25, endpoint=True, base=10.0, dtype=None, axis=0) 
    for thresh in thresh_range:
        clusters = model(points, 100, thresh)
        print("thresh =", thresh)
        print("Number of clusters:", len(clusters))
        print("Clusters:", clusters)
        print("=======")
    # clusters = model(points, 100, 0.01)
    # print(clusters)
    # print("Number of clusters:", len(clusters))
    # print("Clusters:", clusters)

color_list = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'pink', 'brown', 
              'black']  
for i, cluster in enumerate(clusters):
    cluster_points = np.array(cluster.points)
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color_list[i % len(color_list)], label=f'Cluster {i+1}')

plt.title("Final Clusters")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()


    
