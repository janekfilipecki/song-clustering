from sklearn.metrics import silhouette_score
import typing
from preprocess import preprocess


def get_sihlouette_score(raw_data_folder_path, playlists: typing.List[str]):
    # the data should onlu contain numerical columns
    # playlists are meant to be lists of track_ids

    numerical_columns = ['popularity', 'duration_ms',
                         'danceability', 'energy', 'key', 'loudness',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo',
                         'popularity_from_sessions', 'release_date_numeric']

    data = preprocess(raw_data_folder_path, numerical_columns)

    for label, playlist in enumerate(playlists):
        for track in playlist:
            data.loc[data['track_id'] == track, "label"] = label
    data_numerical = data[numerical_columns].copy()
    data_numerical["label"] = data["label"]
    data_numerical.dropna(subset=["label"], inplace=True)
    labels = data_numerical['label'].values
    return silhouette_score(data_numerical, labels)
