import os
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from data_processing import CLUSTER_ATTRIBUTES, TrialManager
from pprint import pprint
import pandas as pd
import sklearn.linear_model


trial_manager = TrialManager()


def calculate_counts():
    counts = {}
    for attribute in CLUSTER_ATTRIBUTES:
        counts[attribute] = attribute_counts = {}
        for x in ("largest", "smallest"):
            attribute_counts[x] = lar_sma_counts = {}
            for y in ("first", "last"):
                lar_sma_counts[y] = 0

    n_trials = 0
    for trial in trial_manager.trials():
        n_trials += 1
        for attribute in CLUSTER_ATTRIBUTES:
            for x in ("largest", "smallest"):
                for y in ("first", "last"):
                    counts[attribute][x][y] += 1 if trial["cluster_attributes_first_last"][attribute][x][y] else 0
    return counts, n_trials

def calculate_relative_counts():
    relative_counts, n_trials = calculate_counts()

    for attribute in CLUSTER_ATTRIBUTES:
            for x in ("largest", "smallest"):
                for y in ("first", "last"):
                    relative_counts[attribute][x][y] = relative_counts[attribute][x][y] / n_trials

    return relative_counts

pprint(calculate_relative_counts())

def generate_clusters_dataframe():
    rows = []
    for trial in trial_manager.trials():
        for idx, cluster in enumerate(trial["clusters"]):
            row = {}
            for key in ("participant_id", "trial_number", "number_of_points", "group", "base_uuid"):
                row[key] = trial[key]
            for attribute in CLUSTER_ATTRIBUTES:
                attribute_value = cluster[attribute]
                row[attribute] = attribute_value
            row["cluster_idx"] = idx
            rows.append(row)
    return pd.DataFrame.from_records(rows)


df = generate_clusters_dataframe()

os.makedirs("build/attribute-stimulus-graphs", exist_ok=True)
os.makedirs("build/attribute-r2-slope-graphs", exist_ok=True)
os.makedirs("build/attribute-stimulus-median-graphs", exist_ok=True)


def scale_series(x):
    min = np.min(x)
    max = np.max(x)
    if min == max:
        return 1
    return (x - min) / (max - min)

def create_attribute_graphs(df, *, attributes=CLUSTER_ATTRIBUTES, x_column = "cluster_idx",
                            median_graphs=True,
                            stimulus_graphs=True,
                            r2_slope_graphs=True,
                            stimulus_graph_alpha: float=1.0):

    if stimulus_graphs:
        for attribute in attributes:
            for key, stim_df in df.groupby(['base_uuid']):
                r2s = []
                slopes = []
                fig, ax = plt.subplots()
                stim = key
                for key, group_df in stim_df.groupby(['participant_id']):
                    # participant_id = key
                    if len(group_df) <= 2:
                        continue
                    mod = sklearn.linear_model.LinearRegression()
                    group_df.sort_values([x_column], inplace=True)
                    y = group_df[attribute].to_numpy()
                    X = group_df[x_column].to_numpy().reshape(-1, 1)
                    mod.fit(X, y)
                    slope = mod.coef_[0]
                    r2 = mod.score(X, y)
                    r2s.append(r2)
                    slopes.append(slope)
                    ax.plot(X[:, 0], y, alpha=stimulus_graph_alpha)
                attribute_stimulus_filename = f"{attribute}_{stim}.png"
                fig.savefig(os.path.join("build/attribute-stimulus-graphs", attribute_stimulus_filename))
                plt.close(fig)

                if r2_slope_graphs:
                    # graphing the histograms of the R2s
                    fig, ax = plt.subplots(ncols=2)
                    ax[0].hist(r2s)
                    ax[0].set_title("R2s")
                    ax[1].hist(slopes)
                    ax[1].set_title("Slopes")
                    fig.savefig(os.path.join("build/attribute-r2-slope-graphs", f"{attribute}.png"))
                    plt.close(fig)

    if median_graphs:
        for attribute in attributes:
            for key, stim_df in df.groupby(["base_uuid"]):
                stim = key
                grouped = stim_df.groupby([x_column]).agg({attribute: "median"}).reset_index()
                fig, ax = plt.subplots()
                ax.plot(grouped[x_column], grouped[attribute])
                attribute_stimulus_filename = f"{attribute}_{stim}.png"
                fig.savefig(os.path.join("build/attribute-stimulus-median-graphs", attribute_stimulus_filename))
                plt.close(fig)

def relative_measures(df: pd.DataFrame):
    df = df.copy()
    
    def application_function(frame):
        frame = frame.copy()
        frame["rel_cluster_idx"] = scale_series(frame["cluster_idx"])
        for attribute in CLUSTER_ATTRIBUTES:
            
            frame["rel_" + attribute] = scale_series(frame[attribute])
            
            assert not np.any(np.isnan(frame["rel_" + attribute])), f"{attribute} contains NaNs!"
        return frame
    
    return df.groupby(['participant_id', 'trial_number']).apply(application_function)
    
create_attribute_graphs(relative_measures(df), attributes=["rel_" + x for x in CLUSTER_ATTRIBUTES],
                        x_column="rel_cluster_idx", stimulus_graph_alpha=0.1)


        
print(df[(df["participant_id"] == 1) & (df["trial_number"] == 1)].to_string())



# plt.hist(r2s)
# plt.show()



# def tmp():
#     for trial in trial_manager.trials():
#         for cluster in trial["clusters"]:
#             if cluster["numerosity"] > 2:
#                 yield cluster["linearity"]

# r2_values = list(tmp())
# print(np.mean(r2_values))
# plt.hist(r2_values)
# plt.show()

# import random

# def tmp1():
#     for i in range(n_trials):
#         points = []
#         for n in range(25):
#             x = random.randint(0, 800)
#             y = random.randint(0, 500)
#             points.append(dict(x=x, y=y))
#         yield utils.linearity(points)

# plt.hist(list(tmp1()))
# plt.show()





# something is special
#




# fig, axes = plt.subplots(nrows=2)

# for ax, key in zip(axes, ("first", "last")):
#     ax.bar(list(range(len(largest_counts.keys()))), [largest_counts["area"][key],
#                                                       largest_counts["density"][key],
#                                                       largest_counts["numerosity"][key]],
#            tick_label=["area", "density", "numerosity"])
#     ax.set_title(key + ", largest")



# plt.show()

# print(largest_counts, smallest_counts)
