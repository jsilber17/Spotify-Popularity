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
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


class SpotifyPlaylist(object):
    def __init__(self, client_id, client_secret, user_id, playlist_id, id_list=[]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.id_list = id_list
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(self.client_id, self.client_secret))


    def create_list_of_ids_for_playlist(self):
        playlist_content = self.sp.user_playlist(self.user_id, self.playlist_id)

        for key,val in enumerate(playlist_content['tracks']['items']):
            self.id_list.append(val['track']['id'])

        return self.id_list


    def get_data_on_one_track(self, track_id):
        ''''
        input: track_id to analyze
        output: a list of audio featusp.Spotify(client_credentials_manager=SpotifyClientCredentialsres for the track
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
    five_playlist_ids = [sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['id'] for num in range(10)]
    five_playlist_usernames = [(client_id, client_secret, sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['owner']['id']) for num in range(10)]
    d_genre_playlists = dict(zip(five_playlist_ids, five_playlist_usernames))

    # five_SpotifyPlaylists = [SpotifyPlaylist(d_genre_playlists[key][0], d_genre_playlists[key][1], d_genre_playlists[key][2], key).compile_all_track_data() for key in d_genre_playlists]
    playlist_1 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[0]).compile_all_track_data()
    playlist_2 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[1]).compile_all_track_data()
    playlist_3 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[2]).compile_all_track_data()
    playlist_4 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[3]).compile_all_track_data()
    playlist_5 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[4]).compile_all_track_data()
    playlist_6 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[5]).compile_all_track_data()
    playlist_7 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[6]).compile_all_track_data()
    playlist_8 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[7]).compile_all_track_data()
    playlist_9 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[8]).compile_all_track_data()
    playlist_10 = SpotifyPlaylist(client_id, client_secret, d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[9]).compile_all_track_data()

    final_playlist = playlist_1 + playlist_2 + playlist_3 + playlist_4 + playlist_5 + playlist_6 + playlist_7 + playlist_8 + playlist_9 + playlist_10

    df = pd.DataFrame(final_playlist, columns=['track', 'artist', 'album', 'popularity', 'time', 'release_date',
                                                'track_number', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                                'speechiness', 'acoustincess', 'instrumentalness', 'liveness',
                                                'valence', 'tempo', 'time_signature'])

    df['genre'] = genre

    return(df)


def DataFrame_to_CSV(df, path):
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
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'metal'),"~/galvanize/capstones/capstone_1/metal.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'folk'),"~/galvanize/capstones/capstone_1/folk.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'indie'),"~/galvanize/capstones/capstone_1/indie.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'alternative'),"~/galvanize/capstones/capstone_1/alternative.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre('f1e0972287e94005ab6fe832983b376c','daf5efbba5044c5cb1362a8a3609ab2d', 'world'),"~/galvanize/capstones/capstone_1/world.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'funk'),"~/galvanize/capstones/capstone_1/funk.csv")
    DataFrame_to_CSV(SpotifyPlaylists_by_genre(client_id, client_secret, 'show tune'),"~/galvanize/capstones/capstone_1/show_tune.csv")
if __name__ == "__main__":
    main()



#list of genres:
    #rock and roll, R+B, Pop, Country, Latin, Electronic, Christian, Jazz, Classical, Seasonal








# def list_of_SpotifyPlaylists_by_genre(client_id, client_secret, genre):
#     ten_playlist_ids = [sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['id'] for num in range(5)]
#     ten_playlist_usernames = [(client_id, client_secret, sp.search(q=str(genre), limit=10, type='playlist')['playlists']['items'][num]['owner']['id']) for num in range(5)]
#     d_genre_playlists = dict(zip(ten_playlist_ids, ten_playlist_usernames))
#
#     # first_playlist = SpotifyPlaylist(d_genre_playlists[list(d_genre_playlists.keys())[0]][0], d_genre_playlists[list(d_genre_playlists.keys())[0]][1], d_genre_playlists[list(d_genre_playlists.keys())[0]][2], list(d_genre_playlists.keys())[0]).compile_all_track_data()
#     # five_spotify_playlists = [SpotifyPlaylist(d_genre_playlists[key][0], d_genre_playlists[key][1], d_genre_playlists[key][2], key).compile_all_track_data() for key in d_genre_playlists]
#     list_objects = np.array([SpotifyPlaylist(d_genre_playlists[key][0], d_genre_playlists[key][1], d_genre_playlists[key][2], key) for key in d_genre_playlists])
#     playlist_func = lambda x: x.compile_all_track_data()
#     vec_func = np.vectorize(playlist_func)
#     Spotify_list = vec_func(list_objects)
#     # ten_SpotifyPlaylists = [SpotifyPlaylist(d_genre_playlists[key][0], d_genre_playlists[key][1], d_genre_playlists[key][2], key).compile_all_track_data() for key in d_genre_playlists]
#     return Spotify_list
