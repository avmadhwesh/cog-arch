from .classes import ClusterTrial
import pathlib
import json
from .classes import Cluster
from copy import copy
import pandas as pd
import numpy as np
import scipy
import warnings

def get_trials():
    all_trials = []
    for path in pathlib.Path("data/normalized_clustering_trials/").glob("*.json"):
        trials = json.loads(path.read_bytes())
        for t in trials:
            all_trials.append(ClusterTrial.from_data_dict(t))
    return all_trials

def get_clusters_dataframe():

    rows = []
    for t in get_trials():
        base = {}
        base["trial_number"] = t.trial_number
        base["participant_id"] = t.participant_id
        base["cluster_structure"] = t.group
        base["number_of_points"] = t.number_of_points
        base["silhouette_score"] = t.silhouette_score
        base["calinski_harabasz_score"] = t.calinski_harabasz_score
        base["davies_bouldin_score"] = t.davies_bouldin_score
        base['base_uuid'] = t.base_uuid
        base['experiment_version'] = t.experiment_version

                
        for c in t.clusters:
            row = copy(base)
            for attribute_name in Cluster.attributes:
                row[attribute_name] = (getattr(c, attribute_name))

            row['even_spacing'] = c.even_spacing

            cluster_points = np.array([(a["x"], a["y"]) for a in c.points])
            
            def check_normality(values):
                return scipy.stats.normaltest(values).pvalue
            

            if len(cluster_points) >= 8:
                with warnings.catch_warnings():
                    # kurtosis test needs 20 samples for a good
                    # estimate, but we don't have that here in many
                    # cases, so turning off warnings
                    warnings.simplefilter("ignore")
                    row['cluster_normality_x'] = check_normality(cluster_points[:, 0])
                    row['cluster_normality_y'] = check_normality(cluster_points[:, 1])
                
            else:
                row['cluster_normality_x'] = float('nan')
                row['cluster_normality_y'] = float('nan')
                
            row["duration"] = c.duration
            row["cluster_index"] = c.cluster_index
            row['start_time'] = c.start_time - t.start_timestamp
            rows.append(row)

    return pd.DataFrame.from_records(rows)

