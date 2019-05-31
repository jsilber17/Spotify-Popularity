import numpy as np
import pandas as pd
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
import os

#INITIALIZE THE SPOTIFY API WITH CREDENTIALS
client_id = os.environ['SPOTIFY_API_KEY']
client_secret = os.environ['SPOTIFY_API_SECRET_KEY']
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def create_spotify_instance(client_id, client_secret):
    '''Initializes an instance with the Spotify API Web Client'

    Input: Client Id, Client Secret --> both given to developer from Spotify API
    Output: Spotify Instance --> Alias all Spotify Functions with this obect
    '''

    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


class SpotifyPlaylist(object):
    '''
    SpotifyPlaylist is a list of lists and each list represents one track from the playlist; the list of list is one full playlist
    '''
    def __init__(self, client_id, client_secret, user_id, playlist_id, id_list=[]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.id_list = id_list
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(self.client_id, self.client_secret))


    def create_list_of_ids_for_playlist(self):
        '''
        Returns list of track Ids for all of the tracks in one playlist from Spotify
        '''
        playlist_content = self.sp.user_playlist(self.user_id, self.playlist_id)

        for key,val in enumerate(playlist_content['tracks']['items']):
            self.id_list.append(val['track']['id'])

        return self.id_list


    def get_data_on_one_track(self, track_id):
        ''''
        Input: Track_ID to analyze
        Output: A list of audio features for the track
        '''
        data = self.sp.track(track_id)
        features = self.sp.audio_features(track_id)[0]

        track = data['name']
        artist = data['album']['artists'][0]['name']
        album = data['album']['name']
        popularity = data['popularity']
        time = data['duration_ms']
        release_date = data['album']['release_date']
        track_number = data['track_number']

        danceability = features['danceability']
        energy = features['energy']
        key = features['key']
        loudness = features['loudness']
        mode = features['mode']
        speechiness = features['speechiness']
        acoustincess = features['acousticness']
        instrumentalness = features['instrumentalness']
        liveness = features['liveness']
        valence = features['valence']
        tempo = features['tempo']
        time_signature = features['time_signature']

        return [track, artist, album, popularity, time, release_date,
                track_number, danceability, energy, key, loudness, mode,
                speechiness, acoustincess, instrumentalness, liveness,
                valence, tempo, time_signature]


    def compile_all_track_data(self):
        '''
        Returns a list of lists --> Final product for a SpotifyPlaylist
        '''
        self.id_list = []
        self.id_list = self.create_list_of_ids_for_playlist()
        list_track_info = []
        for i in range(len(self.id_list)):
            time.sleep(0.5)
            track = self.get_data_on_one_track(self.id_list[i])
            list_track_info.append(track)
        return list_track_info


    def __add__(self, other):
        return self.compile_all_track_data.extend(other.compile_all_track_data)


    def __eq__(self, other):
        return self.compile_all_track_data == other.compile_all_track_data


def SpotifyPlaylists_by_genre(client_id, client_secret, genre):
    '''
    Input: ClientID, ClientSecret, playlist genre
    Output: Returns a 10 SpotifyPlaylists merged together in a Pandas DataFrame to create a larger SpotifyPlaylist based on the genre provided by the user
    '''
    five_playlist_ids = [sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['id'] for num in range(10)]
    five_playlist_usernames = [(client_id, client_secret, sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['owner']['id']) for num in range(10)]
    d_genre_playlists = dict(zip(five_playlist_ids, five_playlist_usernames))

    final_playlist = []

    for i in range(0, 10):
        playlist = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[i]).compile_all_track_data()
        final_playlist += playlist

    df = pd.DataFrame(final_playlist, columns=['track', 'artist', 'album', 'popularity', 'time', 'release_date',
                                                'track_number', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                                'speechiness', 'acoustincess', 'instrumentalness', 'liveness',
                                                'valence', 'tempo', 'time_signature'])
    df['genre'] = genre

    return(df)


def DataFrame_to_CSV(df, path):
    '''
    Converts the DataFrame for the large SpotifyPlaylist into an exported CSV file
    '''
    return df.to_csv(path)

def main():
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'rock'),"~/galvanize/capstones/capstone_1/rock.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'rhythm and blues'),"~/galvanize/capstones/capstone_1/rb.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'pop'),"~/galvanize/capstones/capstone_1/pop.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'country'),"~/galvanize/capstones/capstone_1/country.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'latin'),"~/galvanize/capstones/capstone_1/latin.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'electronic'),"~/galvanize/capstones/capstone_1/electronic.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'hip hop'),"~/galvanize/capstones/capstone_1/hip_hop.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'jazz'),"~/galvanize/capstones/capstone_1/jazz.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'classical'),"~/galvanize/capstones/capstone_1/classical.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'seasonal'),"~/galvanize/capstones/capstone_1/seasonal.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'metal'),"~/galvanize/capstones/capstone_1/metal.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'folk'),"~/galvanize/capstones/capstone_1/folk.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'indie'),"~/galvanize/capstones/capstone_1/indie.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'alternative'),"~/galvanize/capstones/capstone_1/alternative.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'world'),"~/galvanize/capstones/capstone_1/world.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'funk'),"~/galvanize/capstones/capstone_1/funk.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'show tune'),"~/galvanize/capstones/capstone_1/show_tune.csv")
if __name__ == "__main__":
    main()
