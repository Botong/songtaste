# Imports
import os
import jinja2
from flask import render_template, Flask
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


@app.route('/search/<name>')
def search(name):
    data = search_by_artist_name(name)
    api_url = data['artists']['href']
    items = data['artists']['items']
    html = render_template('search.html',
                           artist_name=name,
                           results=items,
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


@app.route('/teamInfo')
def teamInfo():
    template = JINJA_ENVIRONMENT.get_template('templates/teamInfo.html')
    return template.render()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
