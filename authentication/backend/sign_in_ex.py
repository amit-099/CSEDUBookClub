import os
try:
    from urllib.request import Request,urlopen, URLError
except ImportError:
    from urllib2 import Request,urlopen,URLError

import pyrebase
from flask import *

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'frontend')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir,"assssssssssssssssssssssssssssd")
app = Flask(__name__,template_folder=template_dir)

config = {
    "apiKey": "AIzaSyCsjtdtW4x2YEZxLhnQmqtiBOO-5w22bZQ",
    "authDomain": "searchify-e7016.firebaseapp.com",
    "databaseURL": "https://searchify-e7016.firebaseio.com",
    "projectId": "searchify-e7016",
    "storageBucket": "searchify-e7016.appspot.com",
    "serviceAccount": "/home/amit/PycharmProjects/searchify-e7016-firebase-adminsdk-7g8z4-0bbb2c89df.json",
    "messagingSenderId": "934668298736"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def register(email, password):

    my_data = dict()
    my_data["email"] = email
    my_data["password"] = password
    my_data["returnSecureToken"] = True

    json_data = json.dumps(my_data).encode()
    headers = {"Content-Type": "application/json"}
    request = Request("https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key="+"AIzaSyCsjtdtW4x2YEZxLhnQmqtiBOO-5w22bZQ", data=json_data, headers=headers)

    try:
        loader = urlopen(request)
    except URLError as e:
        message = json.loads(e.read())
        print(message["error"]["message"])
    else:
        print(loader.read())


@app.route('/', methods=['GET', 'POST'])
def basic():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('signup.html', s=successful)
        except:
            return render_template('signup.html', us=unsuccessful)

    return render_template('signup.html')


if __name__ == '__main__':
    register('abc@abc.com', 'abcdabcd')
    app.debug = True
    app.run()
