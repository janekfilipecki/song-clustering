import wandb
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

wandb.login()


wandb.init(project="ium-projekt", entity="ium-team",
           group="k-means", name="num cluster expermient")


data = df = pd.read_json(
    "../../data_v3/data/preprocessed_tracks.jsonl", lines=True)

numerical_columns = ['popularity', 'duration_ms',
                     'danceability', 'energy', 'key', 'loudness',
                     'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo',
                     'popularity_from_sessions', 'release_date_numeric']

data_numerical = data[numerical_columns]

for k in range(2, 50, 3):
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(data_numerical)
    labels = kmeans.labels_

    inertia = kmeans.inertia_
    wandb.log({"num_clusters": k})
    wandb.log({"inertia": inertia})
    wandb.log({"silhouette_score": silhouette_score(data_numerical, labels)})

wandb.finish()
