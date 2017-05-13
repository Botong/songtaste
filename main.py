# Imports
import os
import jinja2
from flask import render_template, request, redirect, url_for, Flask
from spotify import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
app = Flask(__name__, template_folder='templates')


# @app.route('/')
# def index():
#     template = JINJA_ENVIRONMENT.get_template('templates/index.html')
#     return template.render()

@app.route('/')
def homepage():
    html = render_template('homepage.html')
    return html


@app.route('/search', methods=['POST'])
def search():
    name = request.form['artist']
    data = search_by_artist_name(name)
    image = None
    if not data['artists']['items']:
        data = search_by_track_name(name)
        api_url = data['tracks']['href']
        items = data['tracks']['items']
        # print data['tracks']['items'][0]['artists']
        type = 'track'
    else:
        api_url = data['artists']['href']
        items = data['artists']['items']
        type = 'artist'
    html = render_template('search.html',
                           item_name=name,
                           results=items,
                           type=type,
                           api_url=api_url)
    return html


@app.route('/artist/<id>')
def artist(id):
    artist = get_artist(id)

    if artist['images']:
        image_url = artist['images'][0]['url']
    else:
        image_url = 'http://placecage.com/600/400'

    tracksdata = get_artist_top_tracks(id)
    tracks = tracksdata['tracks']

    artistsdata = get_related_artists(id)
    relartists = artistsdata['artists']
    html = render_template('artist.html',
                           artist=artist,
                           related_artists=relartists,
                           image_url=image_url,
                           tracks=tracks)
    return html


@app.route('/artist/<artist_id>/track/<track_id>')
def track(artist_id, track_id):
    artist_info = get_artist(artist_id)
    features = get_track_audio_features(track_id)
    recommend = get_recommendation(track_id, artist_id)
    html = render_template('track.html',
                           features=features,
                           artist=artist_info,
                           recommendation=recommend)
    return html


@app.route('/quality')
def quality():
    template = JINJA_ENVIRONMENT.get_template('templates/DataQuality.html')
    return template.render()


@app.route('/usertest')
def usertest():
    template = JINJA_ENVIRONMENT.get_template('templates/UserTest.html')
    return template.render()


@app.route('/poster')
def poster():
    template = JINJA_ENVIRONMENT.get_template('templates/Poster.html')
    return template.render()


def build_tree(tree, song_list, features, index, depth, max_num):
    tree['name'] = song_list[index]['name']
    tree['artist'] = song_list[index]['artists'][0]
    tree['features'] = features[index]
    tree['preview_url'] = song_list[index]['preview_url']

    count = 1

    if count >= max_num or index + count >= len(song_list):
        return count
    if depth < 4:
        tree['children'] = []
        for i in range(3):
            if count >= max_num or index + count >= len(song_list):
                return count
            node = {}
            count += build_tree(node, song_list, features, index + count, depth+1, max_num/3)
            tree['children'].append(node)

    return count


def generate_recommendation_tree(song_list, features):
    tree = {}
    build_tree(tree, song_list, features, 0, 0, len(song_list))
    return tree


@app.route('/recommendation/<artist_id>/<track_id>')
def recommendation(artist_id, track_id):
    # artist_info = get_artist(artist_id)
    # features = get_track_audio_features(track_id)
    song_list = get_recommendation(track_id, artist_id)['tracks']
    song_list.insert(0, get_a_track(track_id))

    track_ids = []
    for t in song_list:
        track_ids.append(t['id'])

    features = get_several_track_features(track_ids)['audio_features']

    tree = generate_recommendation_tree(song_list, features)
    #
    return json.dumps(tree)
    # return json.dumps(recommend)


@app.route('/teamInfo')
def teamInfo():
    template = JINJA_ENVIRONMENT.get_template('templates/teamInfo.html')
    return template.render()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
