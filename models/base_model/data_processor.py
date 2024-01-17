import pandas as pd
from pprint import pprint
from collections import Counter


class DataProcessor:
    def __init__(self):
        self.artists = pd.read_json('data/artists.jsonl', lines=True)
        self.sessions = pd.read_json('data/sessions.jsonl', lines=True)
        self.tracks = pd.read_json('data/tracks.jsonl', lines=True)
        self.users = pd.read_json('data/users.jsonl', lines=True)


    def get_genres(self):
        genres_counter = Counter(genre for row in self.artists['genres'] for genre in row)
        genres = pd.DataFrame.from_dict(genres_counter, orient='index', columns=['count'])
        genres.reset_index(inplace=True)
        genres.columns = ['genre', 'count']
        return genres

    
    def extend_songs(self):
        songs = pd.merge(self.tracks, self.artists[['id', 'genres']], how='left', left_on='id_artist', right_on='id')
        songs.drop(columns=['id_y'], inplace=True)
        songs.rename(columns={'id_x': 'id'}, inplace=True)
        songs.drop_duplicates(subset=['id'], inplace=True)
        songs.sort_values(by=['popularity'], ascending=False, inplace=True)
        return songs
    

    def get_song_duration(self):
        return {idx : dur for idx, dur in zip(self.extend_songs()['id'], self.extend_songs()['duration_ms'])}
    

    def get_song_popularity(self):
        return {idx : pop for idx, pop in zip(self.extend_songs()['id'], self.extend_songs()['popularity'])}
