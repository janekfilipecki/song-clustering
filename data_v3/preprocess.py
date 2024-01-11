import os
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import time


raw_data_folder_path = '../data_v2/data/'
target_data_folder_path = './data/'
numerical_columns = ['popularity', 'duration_ms', 'explicit',
                     'danceability', 'energy', 'key', 'loudness',
                     'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                     'valence', 'tempo', 'popularity_from_sessions', 'release_date_numeric']


files = os.listdir(raw_data_folder_path)

raw_data = {}

for file in files:
    file_path = os.path.join(raw_data_folder_path, file)
    df = pd.read_json(file_path, lines=True)
    raw_data[file] = df
# initialize dataframes
sessions_df = raw_data['sessions.jsonl']
tracks_df = raw_data['tracks.jsonl']
artists_df = raw_data['artists.jsonl']
# calculate new popularity metric
track_appearance_counts = sessions_df['track_id'].value_counts()
track_appearance_counts = track_appearance_counts.reindex(
    tracks_df['id'], fill_value=0)
event_map = {'play': 1, 'skip': -1, 'like': 2, 'advertisement': 0}
sessions_df['popularity_coefficient'] = sessions_df['event_type'].map(
    event_map)
popularity_per_track = sessions_df.groupby(
    'track_id')['popularity_coefficient'].sum().reset_index()
popularity_per_track.rename(
    columns={'popularity_coefficient': 'popularity_from_sessions'}, inplace=True)
# merge popularity metric with tracks dataframe
tracks_with_popularity = pd.merge(
    tracks_df, popularity_per_track, left_on='id', right_on='track_id', how='left')
# merge tracks dataframe with artists dataframe
tracks_with_popularity_artists = pd.merge(
    tracks_with_popularity, artists_df, left_on='id_artist', right_on='id', how='left')
# delete redundant columns
tracks_with_popularity_artists.drop(
    columns=['track_id', 'id_artist'], inplace=True)
# rename columns
tracks_with_popularity_artists.rename(
    columns={'id_x': 'track_id', 'name_x': 'track_name', 'id_y': 'artist_id', 'name_y': 'artist_name'}, inplace=True)
# convert date column
tracks_with_popularity_artists['release_date_numeric'] = pd.to_datetime(
    tracks_with_popularity_artists['release_date'], format='mixed').apply(
    lambda x: time.mktime(x.timetuple()) if not pd.isnull(x) else None)
# normalize numerical columns
scaler = MinMaxScaler()
tracks_with_popularity_artists_scaled = tracks_with_popularity_artists.copy()
tracks_with_popularity_artists_scaled[numerical_columns] = scaler.fit_transform(
    tracks_with_popularity_artists[numerical_columns])
# save dataframe to json
tracks_with_popularity_artists_scaled.to_json(os.path.join(
    target_data_folder_path, 'preprocessed_tracks.jsonl'), orient='records', lines=True)
