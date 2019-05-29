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


    for i in range(start,stop,skip):
        track_results = sp.search(q=query, type=type, limit=limit,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            artist_name.append(t['artists'][0]['name'])
            track_name.append(t['name'])
            track_id.append(t['id'])
            popularity.append(t['popularity'])


    df = pd.DataFrame(
                            {'artist': artist_name,
                            'track' : track_name,
                            'track_id' : track_id,
                            'popularity' : popularity})
    return df


def DataFrame_to_CSV(df, path):
    return df.to_csv(path)

def main():
    client_id = 'f1e0972287e94005ab6fe832983b376c'
    client_secret = 'daf5efbba5044c5cb1362a8a3609ab2d'
    sp = create_spotify_instance(client_id, client_secret)
    start = 0
    stop = 10000
    skip = 50
    query = 'Phish'
    type = 'artist'
    limit = 50
    df_info = query_to_DataFrame(start, stop, skip, query, type, limit)
    DataFrame_to_CSV(df_info, "~/galvanize/capstones/capstone_1/track_list.csv")
if __name__ == "__main__":
    main()
