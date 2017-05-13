import requests
import base64
import urllib
import urllib2
import json
import time

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
GET_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists?ids={ids}'
GET_SEVERAL_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/tracks/?ids={ids}'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
RELATED_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/related-artists'
TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
GET_TRACK_AUDIO_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features/{id}'
GET_SEVERAL_TRACK_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features/?ids={ids}'
GET_RECOMMENDATION_ENDPOINT = 'https://api.spotify.com/v1/recommendations'
AUTH_ENDPOINT = 'https://accounts.spotify.com/api/token'
GET_ALBUM_ENDPOINT = 'https://api.spotify.com/v1/albums/{id}'
GET_A_TRACK_ENDPOINT = 'https://api.spotify.com/v1/tracks/{id}'
CLIENT_ID = "e812542290fe4c5d832907d8b9f5a0cc"
CLIENT_SECRET = "2421257d44844f35af27e63e7c6499ed"
TOKEN = 'BQAKS9XxiXquOqVpeYJYLGTiCVtNqTbQj2yNOa9SkQkZaMmDNLUOvlmK9s0Ps98HWzxHWWsW4WXJofKj4-mhqA'
TOKEN_EXPIRE_TS = 0


def get_token():
    global TOKEN
    global TOKEN_EXPIRE_TS

    if time.time() <= TOKEN_EXPIRE_TS:
        print('Using previous token: ' + TOKEN)
        return TOKEN

    url = 'https://accounts.spotify.com/api/token'
    authorization = base64.standard_b64encode(CLIENT_ID + ':' + CLIENT_SECRET)

    headers = {
        'Authorization': 'Basic ' + authorization
    }
    data = {
        'grant_type': 'client_credentials',
    }

    data_encoded = urllib.urlencode(data)
    req = urllib2.Request(url, data_encoded, headers)
    response = urllib2.urlopen(req, timeout=30).read()
    response_dict = json.loads(response)

    TOKEN = response_dict['access_token']
    TOKEN_EXPIRE_TS = int(time.time()) + response_dict['expires_in']

    print('Got new token: ' + TOKEN)

    return response_dict['access_token']


# https://developer.spotify.com/web-api/get-artist/
def get_artist(artist_id):
    url = GET_ARTIST_ENDPOINT.format(id=artist_id)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/get-several-artists/
def get_several_artists(artist_ids):
    ids = ','.join(artist_ids)
    url = GET_ARTISTS_ENDPOINT.format(ids=ids)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/search-item/
def search_by_artist_name(name):
    params = {'type': 'artist', 'q': name, 'limit':4}
    resp = requests.get(SEARCH_ENDPOINT, params=params)
    return resp.json()


# https://developer.spotify.com/web-api/search-item/
def search_by_track_name(name):
    params = {'type': 'track', 'q': name, 'limit':5}
    resp = requests.get(SEARCH_ENDPOINT, params=params)
    return resp.json()


# https://developer.spotify.com/web-api/get-related-artists/
def get_related_artists(artist_id):
    url = RELATED_ARTISTS_ENDPOINT.format(id=artist_id)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/get-track/
def get_a_track(track_id):
    url = GET_A_TRACK_ENDPOINT.format(id=track_id)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/get-several-tracks/
def get_several_tracks(track_ids):
    ids = ','.join(track_ids)
    url = GET_SEVERAL_TRACKS_ENDPOINT.format(ids=ids)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/get-artists-top-tracks/
def get_artist_top_tracks(artist_id, country='US'):
    url = TOP_TRACKS_ENDPOINT.format(id=artist_id)
    params = {'country': country}
    resp = requests.get(url, params=params)
    return resp.json()


# https://developer.spotify.com/web-api/get-audio-features/
def get_track_audio_features(track_id):
    headers = {"Authorization": "Bearer " + get_token()}
    url = GET_TRACK_AUDIO_FEATURES_ENDPOINT.format(id=track_id)
    resp = requests.get(url, headers=headers)
    return resp.json()


# https://developer.spotify.com/web-api/get-several-audio-features/
def get_several_track_features(track_ids):
    headers = {"Authorization": "Bearer " + get_token()}
    ids = ','.join(track_ids)
    url = GET_SEVERAL_TRACK_FEATURES_ENDPOINT.format(ids=ids)
    resp = requests.get(url, headers=headers)
    return resp.json()


# https://developer.spotify.com/web-api/get-recommendations/
def get_recommendation(track_id, artist_id):
    headers = {"Authorization": "Bearer " + get_token()}
    params = {'seed_artists': artist_id, 'seed_tracks': track_id, 'limit': 81}
    resp = requests.get(GET_RECOMMENDATION_ENDPOINT, params=params, headers=headers)
    return resp.json()


def get_album(album_id):
    url = GET_ALBUM_ENDPOINT.format(id=album_id)
    resp = requests.get(url)
    return resp.json()