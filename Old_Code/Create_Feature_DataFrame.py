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



def import_track_CSV(path):
    df = pd.read_csv(path)
    return df

def create_track_list(df):
    track_list = []

    for i in df['track_id']:
        track_list.append(i)
    return track_list


def create_audio_feature_column(df, str_aud_feature, track_list):
    if 'Unnamed: 0' in df.columns:
        df = df.drop(['Unnamed: 0'], axis=1)
        feature_dict = {}
    else:
        feature_dict = {}

    for i in track_list[0:10]:
        feature_dict[i] = feature_dict.get(i, sp.audio_features(i)[0][str_aud_feature])

    df_feature = pd.DataFrame.from_dict(feature_dict,orient='index').reset_index().rename(columns={'index': 'track_id', 0: str_aud_feature})
    df_final = df.merge(df_feature, on='track_id')
    return df_final


def DataFrame_to_CSV(df, path):
    return df.to_csv(path)

# danceability, energy, key, loudness, mode, speechiness, acoustincess, instrumentalness, liveness, valence, tempo, duration_ms, time_signature

def main():
    client_id = 'f1e0972287e94005ab6fe832983b376c'
    client_secret = 'daf5efbba5044c5cb1362a8a3609ab2d'
    sp = create_spotify_instance(client_id, client_secret)
    df_info = import_track_CSV('~/galvanize/capstones/capstone_1/track_list.csv')
    track_list = create_track_list(df_info)
    df_danceability = create_audio_feature_column(df_info, 'danceability', track_list)
    df_energy = create_audio_feature_column(df_danceability, 'energy', track_list)
    df_key = create_audio_feature_column(df_energy, 'key', track_list)
    df_loudness = create_audio_feature_column(df_key, 'loudness', track_list)
    df_mode = create_audio_feature_column(df_loudness, 'mode', track_list)
    df_speechiness = create_audio_feature_column(df_mode, 'speechiness', track_list)
    df_acousticness = create_audio_feature_column(df_speechiness, 'acousticness', track_list)
    df_instrumentalness = create_audio_feature_column(df_acousticness, 'instrumentalness', track_list)
    df_liveness = create_audio_feature_column(df_instrumentalness, 'liveness', track_list)
    df_valence = create_audio_feature_column(df_liveness, 'valence', track_list)
    df_tempo = create_audio_feature_column(df_valence, 'tempo', track_list)
    df_duration = create_audio_feature_column(df_tempo, 'duration_ms', track_list)
    DataFrame_to_CSV(df_duration, "~/galvanize/capstones/capstone_1/DF_w_AudioFeatres.csv")
if __name__ == "__main__":
    main()
