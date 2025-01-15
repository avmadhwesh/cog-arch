from dataclasses import dataclass
from typing import List, Optional, Dict
from functools import cached_property
import numpy as np
from . import measures


@dataclass
class Cluster():

    attributes = ['numerosity',
                  'area',
                  'linearity',
                  'density',
                  'convex_hull_point_percentage']
    
    edge_points: List[Dict[str, int]]
    points: List[Dict[str, int]]
    start_time: int
    end_time: int
    cluster_index: int

    def points_as_matrix(self):
        return np.array(self.points_as_tuples())

    def points_as_tuples(self):
        points = []
        for point in self.points:
            points.append((point["x"], point["y"]))
        return points

    def points_as_dicts(self):
        points = []
        for point in self.points:
            points.append(dict(x=point["x"], y=point["y"]))
        return points

    @classmethod
    def from_data_dict(cls, d, idx):
        return cls(edge_points=d["edgePoints"],
                   points=d["points"],
                   start_time=d["start_time"],
                   end_time=d["end_time"],
                   cluster_index=idx)

    @cached_property
    def convex_hull(self):
        return  measures.cluster_convex_hull(self.points_as_tuples())
    

    @cached_property
    def area(self):
        return measures.point_set_area(self.convex_hull)

    @cached_property
    def even_spacing(self):
        return measures.even_spacing(self.points_as_matrix())

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def numerosity(self):
        return len(self.points)

    @cached_property
    def linearity(self):
        if self.numerosity > 1:
            return measures.linearity(self.points_as_dicts())
        else:
            return 0


    @cached_property
    def convex_hull_point_percentage(self):
        return len(self.convex_hull) / self.numerosity

    @cached_property
    def density(self):
        if self.area == 0:
            return 0
        return self.numerosity / self.area

    def get_all_attributes(self):
        d = {}
        for attr in self.attributes:
            d[attr] = getattr(self, attr)
        return d
        

@dataclass
class ClusterTrial():
    start_timestamp: int
    end_timestamp: int
    clusters: List[Cluster]
    base_uuid: str
    unique_uuid: str
    group: str
    number_of_points: int
    std_vaccumed_z_score: float
    flipped: bool
    block: int
    set: int
    experiment_version: int
    participant_id: int
    numberOfTries: Optional[int]
    trial_number: int
    silhouette_score: float
    calinski_harabasz_score: float
    davies_bouldin_score: float

    def points_as_dicts(self):
        points = []
        for cluster in self.clusters:
            for point in cluster.points:
                points.append(dict(x=point["x"], y=point["y"]))
        return points

    def points_as_tuples(self):
        points = []
        for cluster in self.clusters:
            for point in cluster.points:
                points.append((point["x"], point["y"]))
        return points

    @classmethod
    def from_data_dict(cls, d):

        m_points = []
        m_cluster_indexes = []

        
        clusters = [Cluster.from_data_dict(d, idx)
                      for idx, d in enumerate(d["clusters"])]

        for c in clusters:
            M = c.points_as_matrix()
            m_points.append(M)
            m_cluster_indexes.append(np.repeat(c.cluster_index, len(M)))

        points = np.concatenate(m_points)
        cluster_membership = np.concatenate(m_cluster_indexes)

        measures_ = measures.calculate_cluster_goodness_measures(points, cluster_membership)

        return cls(start_timestamp=d["startTimestamp"],
                   end_timestamp=d["endTimestamp"],
                   clusters=clusters,
                   base_uuid=d["base_uuid"],
                   unique_uuid=d["unique_uuid"],
                   group=d["group"],
                   number_of_points=d["number_of_points"],
                   std_vaccumed_z_score=d["std_vaccumed_z_score"],
                   flipped=d["flipped"],
                   block=d["block"],
                   set=d["set"],
                   experiment_version=d["experiment_version"],
                   participant_id=d["participant_id"],
                   numberOfTries=d["numberOfTries"],
                   trial_number=d["trial_number"],
                   silhouette_score=measures_["silhouette_score"],
                   calinski_harabasz_score=measures_["calinski_harabasz_score"],
                   davies_bouldin_score=measures_["davies_bouldin_score"])
