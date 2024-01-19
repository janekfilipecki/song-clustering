import wandb
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np

wandb.login()


wandb.init(project="ium-projekt", entity="ium-team",
           group="dbscan", name="dbscan eps euclidean")


data = df = pd.read_json(
    "../../data_v3/data/preprocessed_tracks.jsonl", lines=True)

numerical_columns = ['popularity', 'duration_ms',
                     'danceability', 'energy', 'key', 'loudness',
                     'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo',
                     'popularity_from_sessions', 'release_date_numeric']

metric = "euclidean"
wandb.log({"metric": metric})

data_numerical = data[numerical_columns]
for eps in np.linspace(0.00001, 1, 10):

    dbscan = DBSCAN(eps=eps, metric=metric)
    dbscan.fit(data_numerical)
    labels = dbscan.labels_

    wandb.log({"eps": eps})
    unique, counts = np.unique(labels, return_counts=True)
    sihlouette = -1
    if len(unique) >= 2:
        sihlouette = silhouette_score(data_numerical, labels)
    wandb.log({"silhouette_score": sihlouette})

wandb.finish()
