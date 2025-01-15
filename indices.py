import numpy as np
from typing import List

def _count_hits(M):
    return np.sum(np.triu(M)) - np.trace(M)

def fowlkes_mallows(cluster_matrix_1, cluster_matrix_2):
    assert cluster_matrix_1.shape == cluster_matrix_2.shape
    N = cluster_matrix_1.shape[0]

    TPS = np.logical_and(cluster_matrix_1, cluster_matrix_2)
    FPS = np.logical_and(cluster_matrix_1, np.logical_not(cluster_matrix_2))
    FNS = np.logical_and(np.logical_not(cluster_matrix_1), cluster_matrix_2)

    TP = _count_hits(TPS)
    FP = _count_hits(FPS)
    FN = _count_hits(FNS)

    if (TP + FP) == 0 or (TP + FN) == 0:
        return 0
    
    return (TP / (TP + FP) * TP / (TP + FN)) ** 0.5

def _pairwise_equal_matrix(a):
    return (a[:, np.newaxis] == a[np.newaxis, :]).astype('uint8')


def to_standard_form(clustering):
    clustering = list(filter(lambda x: len(x) != 0, clustering))
    
    cluster_indexes = []
    for idx, points in enumerate(clustering):
        cluster_indexes.append(np.full((len(points)), idx))

    points = np.concatenate(clustering)
    cluster_indexes = np.concatenate(cluster_indexes)

    sort_indices_1 = np.argsort(points[:, 1], axis=0)
    points = points[sort_indices_1]
    cluster_indexes = cluster_indexes[sort_indices_1]

    sort_indices_2 = np.argsort(points[:, 0], axis=0)
    points = points[sort_indices_2]
    cluster_indexes = cluster_indexes[sort_indices_2]
    return points, cluster_indexes

def to_cluster_matrix(clustering: List[np.ndarray]):
    _, cluster_indexes = to_standard_form(clustering)
    return _pairwise_equal_matrix(cluster_indexes)
    


# C1_pre = [np.array([[0, 1],
#                     [1, 0],
#                     [0, 0]]),
#           np.array([[1, 1]])]

# to_cluster_matrix(C1_pre)

# array([[1, 1, 1, 0],
#        [1, 1, 1, 0],
#        [1, 1, 1, 0],
#        [0, 0, 0, 1]], dtype=uint8)


# Test case

# C1 = [[1, 1, 1, 0],
#       [1, 1, 1, 0],
#       [1, 1, 1, 0],
#       [0, 0, 0, 1]]

# C2 = [[1, 0, 1, 0],
#       [0, 1, 0, 1],
#       [1, 0, 1, 0],
#       [0, 1, 0, 1]]


# fowlkes_mallows(np.array(C1), np.array(C2))

# # 0.4082482904638631

