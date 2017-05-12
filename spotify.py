import requests
import base64
import urllib
import urllib2
import json

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
RELATED_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/related-artists'
TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
GET_TRACK_AUDIO_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features/{id}'
GET_RECOMMENDATION_ENDPOINT = 'https://api.spotify.com/v1/recommendations'
AUTH_ENDPOINT = 'https://accounts.spotify.com/api/token'
CLIENT_ID = "e812542290fe4c5d832907d8b9f5a0cc"
CLIENT_SECRET = "2421257d44844f35af27e63e7c6499ed"
TOKEN = 'BQBb6Lcekdd4_yNc77rO8Fk5R1cuJb0_UdS-LlPx57yFIQH4Su0ZSieJ1mU0ELy5R1QHF0d9d-a3lMq4ogg2nQ'


def authenticate():
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
    return response_dict['access_token']


# https://developer.spotify.com/web-api/get-artist/
def get_artist(artist_id):
    url = GET_ARTIST_ENDPOINT.format(id=artist_id)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/search-item/
def search_by_artist_name(name):
    params = {'type': 'artist'}
    params['q'] = name
    resp = requests.get(SEARCH_ENDPOINT, params=params)
    return resp.json()


# https://developer.spotify.com/web-api/get-related-artists/
def get_related_artists(artist_id):
    url = RELATED_ARTISTS_ENDPOINT.format(id=artist_id)
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
    headers = {"Authorization": "Bearer " + TOKEN}
    url = GET_TRACK_AUDIO_FEATURES_ENDPOINT.format(id=track_id)
    resp = requests.get(url, headers = headers)
    return resp.json()


# https://developer.spotify.com/web-api/get-recommendations/
def get_recommendation(track_id, artist_id):
    params = {'seed_artists': artist_id, 'seed_tracks': track_id}
    resp = requests.get(GET_RECOMMENDATION_ENDPOINT, params)
    return resp.json()