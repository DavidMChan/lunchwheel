import random
import os
import time

from flask import Flask, render_template, redirect, make_response

import requests

# Setup Flask
app = Flask(__name__)
app.secret_key = 'RandomSecretKey'

# DOWNLOAD AND CACHE RESULTS FOR BWW
maps_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
google_api_key = os.environ['GOOGLE_API_KEY']

resp = requests.get('{}?location={},{}&type={}&opennow={}&radius={}&rankby=prominence&key={}'.format(
    maps_url,
    '37.873287',
    '-122.268203',
    'restaurant',
    'true',
    '3000',
    google_api_key,
)).json()

all_places = resp['results']
while 'next_page_token' in resp:
    time.sleep(10)
    resp = requests.get('{}?pagetoken={}&key={}'.format(
        maps_url,
        resp['next_page_token'],
        google_api_key,
    )).json()
    all_places += resp['results']


@app.route('/photo/<id>')
def photo(id):

    response = make_response(
        requests.get('https://maps.googleapis.com/maps/api/place/photo?photoreference={}&key={}&maxheight=500'.format(id, google_api_key))._content)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='image.jpg')
    return response


@app.route('/select')
def select():
    # Pick a set of restaurants from all of the places
    selections = random.sample(all_places, k=5)
    return render_template('selection.html', selections=selections)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=9191)
