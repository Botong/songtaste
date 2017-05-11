import requests

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
RELATED_ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/related-artists'
TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'
GET_MULTI_TRACKS_FEATURES = 'https://api.spotify.com/v1/audio-features?ids={ids}'
GET_TRACK_AUDIO_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features/{id}'
GET_RECOMMENDATION_ENDPOINT = 'https://api.spotify.com/v1/recommendations'


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
    # print resp.json()
    return resp.json()


# https://developer.spotify.com/web-api/get-audio-features/
def get_track_audio_features(track_id):
    url = GET_TRACK_AUDIO_FEATURES_ENDPOINT.format(id=track_id)
    resp = requests.get(url)
    return resp.json()


# https://developer.spotify.com/web-api/get-recommendations/
def get_recommendation(track_id, artist_id):
    params = {'seed_artists': artist_id, 'seed_tracks': track_id}
    resp = requests.get(GET_RECOMMENDATION_ENDPOINT, params)
    return resp.json()