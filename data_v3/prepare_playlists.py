import wandb
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
from preprocess import preprocess


def prepare_playlists(raw_data_folder_path="../data_v2/data/",):

    wandb.login()
    wandb.init(project="ium-projekt", entity="ium-team",
               group="production")

    numerical_columns = ['popularity', 'duration_ms',
                         'danceability', 'energy', 'key', 'loudness',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo',
                         'popularity_from_sessions', 'release_date_numeric']

    data = preprocess(raw_data_folder_path, numerical_columns)
    data_numerical = data[numerical_columns]

    NUM_CLUSTERS = 11

    kmeans = KMeans(n_clusters=NUM_CLUSTERS, n_init=10)
    kmeans.fit(data_numerical)
    labels = kmeans.labels_
    inertia = kmeans.inertia_

    wandb.log({"num_clusters": NUM_CLUSTERS})
    wandb.log({"inertia": inertia})
    wandb.log({"silhouette_score": silhouette_score(data_numerical, labels)})

    data["labels"] = labels
    grouped = data.groupby("labels")
    data["duration_hours"] = data["duration_unscaled"]/3600000
    grouped_dataframes = {label: group_df for label, group_df in grouped}

    playlists = []

    for label, group_df in grouped_dataframes.items():
        # If there arent enough songs in the group, add random songs,
        # that arent already present in the group
        if group_df["duration_hours"].sum() < 1:
            while group_df["duration_hours"].sum() < 1:
                common_rows = pd.merge(
                    data, group_df, how='inner', on='track_id')
                df_excluded = data[~data['track_id'].isin(
                    common_rows['track_id'])]
                random_sample = df_excluded.sample(n=1, replace=False)
                group_df = pd.concat([data, random_sample], ignore_index=True)

        # Get the correct playlist duration

        group_df.sort_values(by="popularity_from_sessions",
                             ascending=False, inplace=True)
        selected_rows = []
        current_playlist_duration = 0
        for index, row in group_df.iterrows():
            selected_rows.append(row)
            current_playlist_duration += row['duration_hours']

            if current_playlist_duration >= 1:
                break

        playlist = pd.DataFrame(selected_rows)
        playlists.append(
            (label, playlist, playlist["popularity_from_sessions"].mean()))

    # Now out of the playlists select the 10 most popular on average
    playlists.sort(key=lambda p: p[2], reverse=True)
    playlists = playlists[:10]

    playlists_list = []
    for _, playlist, _ in playlists:
        playlists_list.append(playlist["track_id"].to_list())

    return playlists_list
