from data_processor import DataProcessor


class BaseModel:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.genres = self.data_processor.get_genres()
        self.songs = self.data_processor.extend_songs()
        self.song_duration = self.data_processor.get_song_duration()
        self.song_popularity = self.data_processor.get_song_popularity()
    

    def categorize_songs(self):
        categorized_songs = {genre : [] for genre in self.genres['genre'].to_list()}
        for genre in categorized_songs.keys():
            for idx in self.songs.index:
                if genre in self.songs['genres'][idx]:
                    categorized_songs[genre].append(self.songs['id'][idx])
        return categorized_songs
    

    def generate_playlists(self):
        playlists = self.categorize_songs()
        playlist_popularity = {genre : [] for genre in self.genres['genre'].to_list()}
        for genre in playlists.keys():
            playlist_duration = 0
            song_pointer = 0
            while playlist_duration <= 3600000 and song_pointer < len(playlists[genre]):
                playlist_duration += self.song_duration[playlists[genre][song_pointer]]
                song_pointer += 1
            playlists[genre] = playlists[genre][:song_pointer]
            numerator = sum(self.song_popularity[song] for song in playlists[genre])
            denominator = len(playlists[genre])
            playlist_popularity[genre] = 0.0 if denominator == 0 else (numerator / denominator)
        top_genres = sorted(playlist_popularity, key=lambda x: playlist_popularity[x], reverse=True)[:10]
        top_playlists = {genre : playlists[genre] for genre in top_genres}
        return top_playlists
    