import os
import random

from authentication.backend.forms import RegistrationForm, LoginForm, Reset, Grades, AddBook

try:
    from urllib.request import Request, urlopen, URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError

import pyrebase
from flask import *

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'frontend')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir, "assssssssssssssssssssssssssssd")
app = Flask(__name__, template_folder=template_dir)

app.config['SECRET_KEY'] = '3qpNfK9CzJLLq0MFHg8RqfUOLCoI3A5wu80CwVVi'

config = {
    "apiKey": "AIzaSyCsjtdtW4x2YEZxLhnQmqtiBOO-5w22bZQ",
    "authDomain": "searchify-e7016.firebaseapp.com",
    "databaseURL": "https://searchify-e7016.firebaseio.com",
    "projectId": "searchify-e7016",
    "storageBucket": "searchify-e7016.appspot.com",
    "serviceAccount": "/home/moumita/PycharmProjects/CSEDUBookClub/searchify-e7016-firebase-adminsdk-7g8z4-0bbb2c89df.json",
    "messagingSenderId": "934668298736"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()


@app.route('/')
def startpage():
    return render_template('startpage.html', auth=auth)


@app.route('/home/<currentuser>')
def home(currentuser):
    # if auth.current_user is None:
    #     flash(f'You have to login first!!!','info')
    #     print("whaaaaaaaa")
    #     return redirect(url_for('login'))
    # else:

    users = db.child("Users").child("Owners").child("UID").get()

    name_list = []
    user_name_list = []

    for user in users.each():
        name_list.append(user.val().get('name'))
        user_name_list.append(user.val().get('username'))

    #print(name, user_name, uid, contact)

    user = auth.current_user
    print(user)

    length = len(name_list)

    return render_template("home.html", auth=auth, user_name_list=user_name_list, name_list=name_list, length=length, currentuser=currentuser)


@app.route('/profile/<user_name>/<currentuser>')
def profile(user_name, currentuser):
    print(user_name)

    books = db.child("Users").child("Owners").child("username").child(user_name).child("books").get()

    book_name_list = []
    book_writer_list = []

    for book in books.each():
        book_name_list.append(book.val().get('name'))
        book_writer_list.append(book.val().get('writer'))

    length = len(book_name_list)

    return render_template("profile.html", auth=auth, book_name_list=book_name_list, book_writer_list=book_writer_list, length=length, currentuser=currentuser)


@app.route('/allbooks/<currentuser>')
def allbooks(currentuser):
    books = db.child("Books").get()

    book_name_list = []
    book_writer_list = []
    book_id_list = []
    book_owner_list = []
    book_avail_list = []
    book_cat_list = []

    for book in books.each():
        book_name_list.append(book.val().get('name'))
        book_writer_list.append(book.val().get('writer'))
        book_id_list.append(book.val().get('bookid'))
        book_owner_list.append(book.val().get('owner'))
        book_avail_list.append(book.val().get('availability'))
        book_cat_list.append(book.val().get('category'))

    length = len(book_name_list)

    return render_template("allbooks.html", auth=auth, book_name_list=book_name_list, book_writer_list=book_writer_list,
                           length=length, book_id_list=book_id_list, book_owner_list=book_owner_list, currentuser=currentuser, book_avail_list=book_avail_list,
                           book_cat_list=book_cat_list)


@app.route('/requests/<currentuser>')
def requests(currentuser):
    print("CCCCCCCCCCCCCCCCCCCCCC        ", currentuser)

    book_name_list = []
    book_writer_list = []
    book_id_list = []
    book_owner_list = []
    book_avail_list = []
    book_cat_list = []
    from_list = []

    all_requests = db.child("Users").child("Owners").child("UID").child(currentuser).child("receiverequest").get()
    #all_requests = dict(all_requests)
    print(type(all_requests))

    # if "receiverequest" in all_requests:
    #     print("yessssssssssssss")
    for aRequest in all_requests.each():
        print("AAAAAAAAAA   ", aRequest.val())
        print(list(aRequest.val()))
        request_condition = list(aRequest.val())
        for val in request_condition:
            if val != 'from':
                print(val)
                p = aRequest.val()
                q = p[val]
                print(q)
                book_name_list.append(q.get('name'))
                book_cat_list.append(q.get('category'))
                book_avail_list.append(q.get('availability'))
                book_id_list.append(q.get('bookid'))
                book_owner_list.append(q.get('owner'))
                book_writer_list.append(q.get('writer'))
            else:
                p = aRequest.val()
                q = p[val]
                from_list.append(q)






        # for key, val in request_condition:
        #     if key != 'from':
        #         req_entry = val
        #         book_name_list.append(req_entry.get('name'))
        #         book_cat_list.append(req_entry.get('category'))
        #         book_avail_list.append(req_entry.get('availability'))
        #         book_id_list.append(req_entry.get('bookid'))
        #         book_owner_list.append(req_entry.get('owner'))
        #         book_writer_list.append(req_entry.get('writer'))
        #     else:
        #         from_list.append(val)

    length = len(book_name_list)
    return render_template("allrequests.html", auth=auth, book_name_list=book_name_list, book_writer_list=book_writer_list,
                           length=length, book_id_list=book_id_list, book_owner_list=book_owner_list,
                           currentuser=currentuser, book_avail_list=book_avail_list,book_cat_list=book_cat_list, from_list=from_list)




@app.route('/addbook/<currentuser>', methods=['GET', 'POST'])
def addbook(currentuser):
    form = AddBook()

    if form.validate_on_submit():
        book_name = form.name.data
        book_writer = form.writer.data
        book_category = form.category.data
        book_availability = form.availability.data

        user_name = db.child("Users").child("Owners").child("UID").child(currentuser).child("username").get().val()
        book_id = user_name + book_name
        print("Booooooooooooooooooooooooookkkkkkkkkkkkkkkidddddddddddd     ", book_id)
        book_owner = user_name

        aBook = {
            'availability': book_availability,
            'bookid': book_id,
            'category': book_category,
            'name': book_name,
            'owner': book_owner,
            'writer': book_writer
        }

        db.child("Books").child(book_id).set(aBook)
        db.child("Users").child("Owners").child("UID").child(currentuser).child("books").child(book_id).set(aBook)
        db.child("Users").child("Owners").child("username").child(user_name).child("books").child(book_id).set(aBook)

        return redirect(url_for('home', currentuser=currentuser))
    return render_template('addbook.html', title='Register', form=form, auth=auth, currentuser=currentuser)


@app.route('/rejected', methods=['POST'])
def rejected():
    book_id = request.form['bookID']
    book_owner = request.form['bookOwner']
    currentuser = request.form['currentuser']
    book_name = request.form['bookName']
    book_writer = request.form['bookWriter']
    book_avail = request.form['bookAvail']
    book_cat = request.form['bookCat']

    user_name = db.child("Users").child("Owners").child("UID").child(currentuser).child("username").get().val()
    db.child("Users").child("Owners").child("UID").child(currentuser).child("receiverequest").child(book_id).remove()
    db.child("Users").child("Owners").child("username").child(user_name).child("receiverequest").child(book_id).remove()

    return json.dumps({'test': 'aaaaaaaaa'})


@app.route('/saveallowed', methods=['POST'])
def saveallowed():
    book_id = request.form['bookID']
    book_owner = request.form['bookOwner']
    currentuser = request.form['currentuser']
    book_name = request.form['bookName']
    book_writer = request.form['bookWriter']
    book_avail = request.form['bookAvail']
    book_cat = request.form['bookCat']
    came_from = request.form['cameFrom']

    aBook = {
        'availability': book_avail,
        'bookid': book_id,
        'category': book_cat,
        'name': book_name,
        'owner': book_owner,
        'writer': book_writer
    }

    user_name = db.child("Users").child("Owners").child("UID").child(currentuser).child("username").get().val()
    #uid_owner = db.child("Users").child("Owners").child("username").child(book_owner).child("UID").get().val()

    db.child("Users").child("Owners").child("UID").child(currentuser).child("allowed").child(book_id).set(aBook)
    db.child("Users").child("Owners").child("username").child(user_name).child("allowed").child(book_id).set(aBook)

    db.child("Users").child("Owners").child("username").child(came_from).child("granted").child(book_id).set(aBook)
    from_uid = db.child("Users").child("Owners").child("username").child(came_from).child("UID").get().val()
    db.child("Users").child("Owners").child("UID").child(from_uid).child("granted").child(book_id).set(aBook)

    return json.dumps({'test': 'aaaaaaaaa'})


@app.route('/savedata', methods=['POST'])
def savedata():
    book_id = request.form['bookID']
    book_owner = request.form['bookOwner']
    currentuser = request.form['currentuser']
    book_name = request.form['bookName']
    book_writer = request.form['bookWriter']
    book_avail = request.form['bookAvail']
    book_cat = request.form['bookCat']



    print("aaaaaaaaaaaaaaaaaaaaaaaaaa                     ", currentuser)
    print(book_id)

    aBook = {
        'availability': book_avail,
        'bookid': book_id,
        'category': book_cat,
        'name': book_name,
        'owner': book_owner,
        'writer': book_writer
    }

    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(6):
        chars.append(random.choice(ALPHABET))
    rand_id = "".join(chars)

    print("Rannnnnnnnnnnnnnnnnnnnndddddddddd           ", rand_id)

    user_name = db.child("Users").child("Owners").child("UID").child(currentuser).child("username").get().val()
    uid_owner = db.child("Users").child("Owners").child("username").child(book_owner).child("UID").get().val()

    print(user_name)

    db.child("Users").child("Owners").child("UID").child(currentuser).child("sentrequest").child(book_id).set(aBook)
    db.child("Users").child("Owners").child("username").child(user_name).child("sentrequest").child(book_id).set(aBook)

    db.child("Users").child("Owners").child("username").child(book_owner).child("receiverequest").child(rand_id).child(book_id).set(aBook)
    db.child("Users").child("Owners").child("username").child(book_owner).child("receiverequest").child(rand_id).child("from").set(user_name)

    db.child("Users").child("Owners").child("UID").child(uid_owner).child("receiverequest").child(rand_id).child(book_id).set(aBook)
    db.child("Users").child("Owners").child("UID").child(uid_owner).child("receiverequest").child(rand_id).child("from").set(user_name)

    return json.dumps({'test': 'aaaaaaaaa'})


@app.route('/about')
def about():
    # if auth.current_user is None:
    #     flash(f'You have to login first!!!','info')
    #     print("whaaaaaaaa")
    #     return redirect(url_for('login'))
    # else:
    return render_template('about.html', title='Damn', auth=auth)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash(f'Account created for {form.username.data}!!', 'success')
        email = form.email.data
        password = form.password.data
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        user_name = form.username.data
        name = form.name.data
        contact = form.contact.data

        print("uuuuuuuuuuuuuuuuuuuuuu    ", uid)

        user_data_uid = {
            'books': 'none',
            'contact no': contact,
            'device_token': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'image': 'false',
            'name': name,
            'username': user_name
        }

        user_data_name = {
            'UID': uid,
            'books': 'none',
            'contact no': contact,
            'image': 'false',
            'name': name
        }

        db.child("Users").child("Owners").child("UID").child(uid).set(user_data_uid)
        db.child("Users").child("Owners").child("username").child(user_name).set(user_data_name)


        return redirect(url_for('home', currentuser=uid))
    return render_template('register.html', title='Register', form=form, auth=auth)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            user = auth.sign_in_with_email_and_password(email, password)
            #user = auth.refresh(user['refreshToken'])
            uid = user['localId']
#            flash(f'You have been logged in!!', 'success')
            return redirect(url_for('home', currentuser=uid))
        except:
            print('danger')
#            flash(f'Log In unsuccessful!!', 'danger')
    return render_template('login.html', title='Login', form=form, auth=auth)


@app.route('/passwordreset', methods=['GET', 'POST'])
def passwordreset():
    form = Reset()
    if form.validate_on_submit():
        email = form.email.data
        auth.send_password_reset_email(email)
        return redirect('login')
    return render_template('ResetPassword.html', title='Reset Password', form=form, auth=auth)


@app.route('/link', methods=['GET', 'POST'])
def link():
    return render_template('link.html', title='Link', auth=auth)


@app.route('/index')
def index():
    if auth.current_user is None:
#        flash(f'You have to login first!!!', 'info')
        print("whaaaaaaaa")
        return redirect(url_for('login'))
    else:
        return render_template('index.html', auth=auth)


@app.route('/grades',methods=['GET','POST'])
def grades():
    if auth.current_user is None:
#        flash(f'You have to login first!!!', 'info')
        print("whaaaaaaaa")
        return redirect(url_for('login'))
    else:
        form = Grades()
        if form.validate_on_submit():
            du = 'No'
            ju = []
            bangla = form.bangla.data
            english = form.english.data
            math = form.math.data
            physics = form.physics.data
            chemistry = form.chemistry.data
            biology = form.biology.data
            ssc = form.ssc.data
            hsc = form.hsc.data
            total = ssc + hsc
            if ssc >= 3.5 and hsc >= 3.5:
                if total >= 8.0:
                    du = 'Yes'
            if total >= 7.5:
                ju.append('A')
            if total >= 8.0:
                ju.append('D')

                if physics >= 4.75 and math >= 4.75:
                    ju.append('H')
            if not ju:
                ju.append('No')
            return render_template('result.html', du=du, ju=ju,auth=auth)

    return render_template('grades.html', title = 'Grades', form=form,auth=auth)



@app.route('/logout')
def logout():
    auth.current_user = None
    return render_template('startpage.html', auth=auth)


if __name__ == '__main__':
    app.debug = True
    app.run()
