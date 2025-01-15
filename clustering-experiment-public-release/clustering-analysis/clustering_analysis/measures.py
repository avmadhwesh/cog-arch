import sklearn.linear_model
import sklearn.metrics
import numpy as np
from typing import List, Tuple
import scipy


def linearity(points):
    points = np.array([[a["x"], a["y"]] for a in points])
    X = points[:, 0].reshape(-1, 1)
    y = points[:, 1]
    model = sklearn.linear_model.LinearRegression()
    model.fit(X, y)
    return model.score(X, y)

## This is for convex hull analyses

def make_stack():
    return []

def stack_pop(stack):
    item = stack[-1]
    stack.pop()
    return item

def stack_push(stack, item):
    stack.append(item)

def stack_length(stack):
    return len(stack)

def stack_to_list(stack):
    return stack


def ccw(a, b, c):
    (x1, y1) = a
    (x2, y2) = b
    (x3, y3) = c
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


def cluster_convex_hull(points: List[Tuple]):
    if len(points) <= 3:
        return points
    points.sort(key=lambda a: a[1])
    points.sort(key=lambda a: a[0])
    stack = make_stack()
    starting_point = points[0]
    stack_push(stack, starting_point)


    def sort_func(a):
        if a[0] == starting_point[0]:
            if a[1] > starting_point[1]:
                return float('inf')
            else:
                return float('-inf')
        else:
            return (a[1] - starting_point[1]) / (a[0] - starting_point[0])

    working_set = sorted(points[1:], key=sort_func)
    for point in working_set:
        while True:
            length = stack_length(stack)
            if length > 2 and ccw(stack[length - 2], stack[length - 1], point) < 0:
                stack_pop(stack)
            else:
                break
        stack_push(stack, point)
    return stack_to_list(stack)

def even_spacing(points):
    if len(points) == 0 or len(points) == 1:
        return 0
    mat = scipy.spatial.distance_matrix(points, points)
    distances = []
    for r in range(mat.shape[0]):
        for c in range(r + 1, mat.shape[1]):
            distances.append(mat[r, c])
    return np.std(distances)

def point_set_area(points: List[Tuple[int, int]]):
    # print(point_set_area([(37, 319), (172, 180), (141, 476)]))
    # 17825.5

    if len(points) <= 2:
        return 0
    points = points.copy()
    points.append(points[0])
    total = 0
    for i in range(0, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        x1, x2 = p1
        y1, y2 = p2
        total += x1 * y2 - x2 * y1
    return 0.5 * abs(total)
    

def calculate_cluster_goodness_measures(points, labels):
    if len(points) == len(np.unique(labels)):
        return dict(silhouette_score=np.nan,
             calinski_harabasz_score=np.nan,
             davies_bouldin_score=np.nan)
        
    return dict(silhouette_score=sklearn.metrics.silhouette_score(points, labels),
                calinski_harabasz_score=sklearn.metrics.calinski_harabasz_score(points, labels),
                davies_bouldin_score=sklearn.metrics.davies_bouldin_score(points, labels))
