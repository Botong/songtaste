# -*- coding: utf-8 -*-
# Imports
import os
import jinja2
from flask import render_template, request, redirect, url_for, Flask
from spotify import *
import math

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
app = Flask(__name__, template_folder='templates')


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
    # artist_info = get_artist(artist_id)
    # features = get_track_audio_features(track_id)
    # recommend = get_recommendation(track_id, artist_id)
    html = render_template('track.html',
                           artist_id=artist_id,
                           track_id=track_id)
    return html


@app.route('/about')
def about():
    html = render_template('about.html')
    return html


@app.route('/data')
def data():
    html = render_template('data.html')
    return html


@app.route('/approach')
def approach():
    html = render_template('approach.html')
    return html


@app.route('/usertest')
def usertest():
    html = render_template('usertest.html')
    return html


@app.route('/poster')
def poster():
    template = JINJA_ENVIRONMENT.get_template('templates/Poster.html')
    return template.render()


# def build_tree_dfs(tree, song_list, features, artists, index, depth, max_num, father):
#     tree['name'] = song_list[index]['name']
#     tree['artist'] = artists[index]
#     tree['features'] = features[index]
#     tree['preview_url'] = song_list[index]['preview_url']
#     if father is not None:
#         tmp = father.copy()
#         tmp.pop('children', None)
#         tmp.pop('father', None)
#         tree['father'] = tmp
#     else:
#         tree['father'] = None
#
#     count = 1
#
#     if count >= max_num or index + count >= len(song_list):
#         return count
#     if depth < 4:
#         tree['children'] = []
#         for i in range(3):
#             if count >= max_num or index + count >= len(song_list):
#                 return count
#             node = {}
#             count += build_tree_dfs(node, song_list, features, artists, index + count, depth+1, max_num/3, tree)
#             tree['children'].append(node)
#
#     return count


# def generate_recommendation_tree(song_list, features, artists):
#     tree = {}
#     build_tree_dfs(tree, song_list, features, artists, 0, 0, len(song_list), None)
#     return tree


def find_most_similar(cur, list, start):
    min_dist = euc_dist(cur, list[start])
    min_idx = start

    for i in range(start + 1, len(list)):
        new_dist = euc_dist(cur, list[i])
        if new_dist < min_dist:
            min_dist = new_dist
            min_idx = i

    return min_idx


def build_tree_dfs(tree, song_list, index, depth, max_num, father):
    tree['name'] = song_list[index]['name']
    tree['artist'] = song_list[index]['artist']
    tree['features'] = song_list[index]['features']
    tree['preview_url'] = song_list[index]['preview_url']
    tree['image'] = song_list[index]['image']
    tree['popularity'] = song_list[index]['popularity']
    if father is not None:
        tmp = father.copy()
        tmp.pop('children', None)
        tmp.pop('father', None)
        tree['father'] = tmp
    else:
        tree['father'] = None

    count = 1

    if count >= max_num or index + count >= len(song_list):
        return count
    if depth < 4:
        tree['children'] = []
        for _ in range(3):
            if count >= max_num or index + count >= len(song_list):
                return count
            node = {}
            new_index = find_most_similar(tree, song_list, index + count)
            song_list[index + count], song_list[new_index] = song_list[new_index], song_list[index + count]
            count += build_tree_dfs(node, song_list, index + count, depth + 1, max_num / 3, tree)
            tree['children'].append(node)

    return count


def build_tree_bfs(tree, song_list):
    item = {'tree': tree, 'depth': 0, 'father': None, 'index': 0}

    queue = [item]
    head = 0
    tail = 1

    count = 1

    while head < tail:
        tree = queue[head]['tree']
        depth = queue[head]['depth']
        father = queue[head]['father']
        index = queue[head]['index']
        head += 1

        if father is not None:
            best_index = find_most_similar(father, song_list, index)
            song_list[index], song_list[best_index] = song_list[best_index], song_list[index]

        tree['name'] = song_list[index]['name']
        tree['artist'] = song_list[index]['artist']
        tree['features'] = song_list[index]['features']
        tree['preview_url'] = song_list[index]['preview_url']
        tree['image'] = song_list[index]['image']
        tree['popularity'] = song_list[index]['popularity']

        if father is not None:
            tmp = father.copy()
            tmp.pop('children', None)
            tmp.pop('father', None)
            tree['father'] = tmp
        else:
            tree['father'] = None

        if depth < 4 and count < len(song_list):
            tree['children'] = []
            child_num = 3 if depth < 3 else 2
            for _ in range(child_num):
                if count < len(song_list):
                    new_node = {}
                    tree['children'].append(new_node)
                    new_item = {'tree': new_node, 'depth': depth + 1, 'father': tree, 'index': count}
                    queue.append(new_item)
                    tail += 1
                    count += 1


def generate_recommendation_tree(song_list):
    tree = {}
    # build_tree_dfs(tree, song_list, 0, 0, len(song_list), None)
    build_tree_bfs(tree, song_list)
    return tree


def euc_dist(s1, s2):
    a = s1['features']
    b = s2['features']
    dist = 0.0
    dist += (a['loudness'] - b['loudness']) ** 2 \
            + (a['tempo'] / 200 - b['tempo'] / 200) ** 2 \
            + (a['valence'] - b['valence']) ** 2 \
            + (a['danceability'] - b['danceability']) ** 2 \
            + (a['energy'] - b['energy']) ** 2 \
            + (a['liveness'] - b['liveness']) ** 2 \
            + (a['acousticness'] - b['acousticness']) ** 2
    return math.sqrt(dist)


@app.route('/recommendation/<artist_id>/<track_id>')
def recommendation(artist_id, track_id):
    # artist_info = get_artist(artist_id)
    # features = get_track_audio_features(track_id)
    song_list = get_recommendation(track_id, artist_id)['tracks']

    song_list.insert(0, get_a_track(track_id))

    track_ids = []
    artist_ids = []
    for t in song_list:
        track_ids.append(t['id'])
        artist_ids.append(t['artists'][0]['id'])

    track_info = get_several_tracks(track_ids[:50])['tracks']
    if len(track_ids) > 50:
        track_info += get_several_tracks(track_ids[50:])['tracks']

    artists = get_several_artists(artist_ids[:50])['artists']

    if len(artist_ids) > 50:
        artists += get_several_artists(artist_ids[50:])['artists']

    features = get_several_track_features(track_ids)['audio_features']

    for i in range(len(song_list)):
        song_list[i]['artist'] = artists[i]
        song_list[i]['popularity'] = track_info[i]['popularity']
        song_list[i]['image'] = track_info[i]['album']['images']
        if len(song_list[i]['image']) > 0:
            song_list[i]['image'] = song_list[i]['image'][2]
        song_list[i]['features'] = features[i]

    remove_list = []

    for i in range(len(song_list)):
        for j in range(i + 1, len(song_list)):
            if song_list[i]['name'] == song_list[j]['name'] and song_list[i]['artist']['name'] == \
                    song_list[j]['artist']['name']:
                remove_list.append(song_list[j])

    for song in remove_list:
        print("removed one duplicate ")
        song_list.remove(song)

    song_list = song_list[0:1] + sorted(song_list[1:], key=lambda s: euc_dist(s, song_list[0]))

    # tree = generate_recommendation_tree(song_list, features, artists)
    tree = generate_recommendation_tree(song_list)
    # print json.dumps(tree)
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
