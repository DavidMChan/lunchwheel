import random
import os

from flask import Flask, render_template

import requests

# Setup Flask
app = Flask(__name__)
app.secret_key = 'RandomSecretKey'

#yclient_id = 'WstnsSg6wn0O0nQE3LNWYQ'
#yapi_key = 'RRa_1MeUAR9XaTDX_qXieecb9_bx4pcQFVguWxxIyfPIZaSbIF2HH0C46vN80kWiCYvFxLaQEd3N4wm3HOIJyKPeeRzeIbzK-LBLvdEP569u-RhTB-jqnQQe9nVEXnYx'


yclient_id = os.environ['YELP_CLIENT_ID']
yapi_key = os.environ['YELP_API_KEY']

@app.route('/select')
def select():

    # Fetch the data from the yelp API
    headers = {'Authorization': 'Bearer {}'.format(yapi_key)}
    resp = requests.get('https://api.yelp.com/v3/businesses/search?term={}&location={}&limit=50&radius=3000'.format(
                        'restaurants', '"2121 Berkeley Way, Berkeley, CA 94704"'),
                        headers=headers)

    # Display a random selection from the JSON
    data = resp.json()

    selection = random.choice(data['businesses'])

    return render_template('selection.html', selection=selection)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run(port=9191)
