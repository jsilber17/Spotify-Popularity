#3 scripts: API call, export_to CSV, pull data in from CSV (or make the api call a function, to csv function)

#Import libraries
import numpy as np
import pandas as pd
import spotipy
import sys
import time
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

#Not sure what this does, but will probably change it
if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Phish'

#Will make this into a helper function
client_id = 'f1e0972287e94005ab6fe832983b376c'
client_secret = 'daf5efbba5044c5cb1362a8a3609ab2d'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Will also make this into a helper function
artist_name = []
track_name = []
track_id = []
popularity = []
duration_ms = []
explicity = []

#Yet another helper function
for i in range(0,10000,50):
    track_results = sp.search(q='year:1995', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        explicity.append(t['explicit'])


def create_pandas_dataframe(artist_lst, track_nm_lst, track_id_lst, popularity_lst):
    df_info = pd.DataFrame(
                            {'artist' : artist_name,
                            'track' : track_name,
                            'track_id' : track_id,
                            'popularity' : popularity})
    return df_info

df_sp = create_pandas_dataframe(artist_name, track_name, track_id, popularity)

df_sp
df_sp.to_csv('track_df')

def create_audio_feature_column(df, aud_feature)
    feature_dict = {}

    for i in track_id[0:10000]:
        feature_column[i] = d_feat.get(i, sp.audio_features(i)[0][str(aud_feature)])

    df_feature = pd.DataFrame.from_dict(feature_dict,orient='index').reset_index().rename(columns={'index': 'track_id', 0: str(aud_feature)})
    return df.merge(df_feature, on='track_id')
