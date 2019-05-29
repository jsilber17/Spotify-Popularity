import numpy as np
import pandas as pd
import spotipy as sp
import time
from spotipy.oauth2 import SpotifyClientCredentials


def create_spotify_instance(id_key, secret_key):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def create_list_of_ids_for_playlist(user_id, playlist_id):
    '''.
    This function grabs all track ids from the playlist it is fed and appends them to a list
    '''
    id_list = []
    playlist_content = sp.user_playlist(user_id, playlist_id)

    for key,val in enumerate(playlist_content['trif __name__ == "__main__":
    main()acks']['items']):
        id_list.append(val['track']['id'])

    return id_list


def get_data_on_one_track(track_id):
    ''''
    input: track_id to analyze
    output: a list of audio features for the track
    '''
    data = sp.track(track_id)
    features = sp.audio_features(track_id)[0]

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


def compile_all_track_data(user_id, playlist_id):
    list_track_info = []
    for i in range(len(create_list_of_ids_for_playlist(user_id, playlist_id))):
        time.sleep(.5)
        track = get_data_on_one_track(create_list_of_ids_for_playlist(user_id, playlist_id)[i])
        list_track_info.append(track)
    return list_track_info


def create_df_from_track_data(list_track_info):
    df = pd.DataFrame(list_track_info, columns=['track', 'artist', 'album', 'popularity', 'time', 'release_date',
                                            'track_number', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                            'speechiness', 'acoustincess', 'instrumentalness', 'liveness',
                                            'valence', 'tempo', 'time_signature'])
    return(df)

def DataFrame_to_CSV(df, path):
    return df.to_csv(path)


def main():
    client_id = 'f1e0972287e94005ab6fe832983b376c'
    client_secret = 'daf5efbba5044c5cb1362a8a3609ab2d'
    sp = create_spotify_instance(client_id, client_secret)
    user_id = 'alanasilber'
    playlist_id = '4Cgw89P3SBngBgjZ8B9Ni8'
    track_list = create_list_of_ids_for_playlist('alanasilber', '0WZaLL5D1WC30IEsM1Upmg')
    playlist = compile_all_track_data(user_id, playlist_id)
    print(playlist)
    # df_play = create_df_from_track_data(playlist)
    # DataFrame_to_CSV(df_play, "~/galvanize/capstones/capstone_1/raw_playlist_data.csv")
if __name__ == "__main__":
    main()

sp.user('spotify')
