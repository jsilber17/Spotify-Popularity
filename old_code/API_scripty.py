import numpy as np
import pandas as pd
import spotipy
import sys
import time
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

def create_spotify_instance(id_key, secret_key):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def query_to_DataFrame(start, stop, skip, query, type, limit):
    artist_name = []
    track_name = []
    track_id = []
    popularity = []
    explicit = []

    for i in range(start,stop,skip):
        track_results = sp.search(q=str(query), type=type, limit=limit,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            artist_name.append(t['artists'][0]['name'])
            track_name.append(t['name'])
            track_id.append(t['id'])
            popularity.append(t['popularity'])
            explict.append(t['explicit'])

    df = pd.DataFrame(
                            {'artist': artist_name,
                            'track' : track_name,
                            'track_id' : track_id,
                            'popularity' : popularity,
                            'explicit' : explicit})
    return df



def create_audio_feature_column(df, str_aud_feature):
    feature_dict = {}

    for i in track_id[0:10000]:
        feature_column[i] = d_feat.get(i, sp.audio_features(i)[0][str_aud_feature])

    df_feature = pd.DataFrame.from_dict(feature_dict,orient='index').reset_index().rename(columns={'index': 'track_id', 0: str_aud_feature})
    df_final = df.merge(df_feature, on='track_id')
    return df_final

# danceability, energy, key, loudness, mode, speechiness, acoustincess, instrumentalness, liveness, valence, tempo, duration_ms, time_signature

def main():
    client_id = 'f1e0972287e94005ab6fe832983b376c'
    client_secret = 'daf5efbba5044c5cb1362a8a3609ab2d'
    sp = create_spotify_instance(client_id, client_secret)
    start = 0
    stop = 10000
    skip = 50
    query = 1995
    type = 'track'
    limit = 50
    df_info = query_to_DataFrame(start, stop, skip, query, type, limit)
    #df_dance = create_audio_feature_column(df_info, 'danceability')
    print(type(df_info))
if __name__ == "__main__":
    main()
