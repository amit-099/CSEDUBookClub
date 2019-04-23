import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from flask import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def basic():
    # Fetch the service account key JSON file contents
    #cred = credentials.Certificate('/home/amit/PycharmProjects/searchify-e7016-firebase-adminsdk-7g8z4-0bbb2c89df.json')
    # Initialize the app with a service account, granting admin privileges
    # firebase_admin.initialize_app(cred, {
    #     'databaseURL': 'https://searchify-e7016.firebaseio.com/'
    # })

    if not len(firebase_admin._apps):
        cred = credentials.Certificate(
            '/home/amit/PycharmProjects/searchify-e7016-firebase-adminsdk-7g8z4-0bbb2c89df.json')
        default_app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://searchify-e7016.firebaseio.com/'
    })

    #ref = db.reference('/')
    ref = db.reference('boxes')
    ref.set({
        'boxes':
            {
                'box001': {
                    'color': 'red',
                    'width': 1,
                    'height': 3,
                    'length': 2
                },
                'box002': {
                    'color': 'green',
                    'width': 1,
                    'height': 2,
                    'length': 3
                },
                'box003': {
                    'color': 'yellow',
                    'width': 3,
                    'height': 2,
                    'length': 1
                }
            }
    })
    return 'abc'


if __name__ == '__main__':
    app.debug = True
    app.run()
